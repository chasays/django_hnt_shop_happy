import json
# from django.db.utils import IntegrityError
# from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from happy_shop.models import (
    HappyShopingCart, HappyShopAddress, HappyShopOrderInfo, HappyShopOrderSKU, 
    HappyShopSKU)
from happy_shop.api.serializers.order import (
    HappyShopingCartSerializer, HappyShopAddressSerializer,
    HappyShopOrderInfoSerializer)
from happy_shop.api.permissions import IsOwnerOrReadOnly


class HappyShopingCartViewsets(viewsets.ModelViewSet):
    """购物车接口
    """
    # 必须登录，并且只返回当前登录用户的数据
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = HappyShopingCartSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return HappyShopingCart.objects.filter(owner=self.request.user, is_del=False)

    def create(self, request, *args, **kwargs):
        """ 重写create方法
        使其重复加入购物车时只修改购买数量
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 重复加入购物车，则进行更新操作
        carts = HappyShopingCart.objects.filter(owner=request.user, sku=serializer.validated_data['sku'])
        if carts.exists():
            instance = carts.first()
            num = serializer.validated_data['num'] + instance.num
            data =  {'num': num, 'sku': instance.sku.id}
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HappyShopAddressViewsets(viewsets.ModelViewSet):
    """收货地址接口
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = HappyShopAddressSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        queryset = HappyShopAddress.objects.filter(is_del=False, owner=self.request.user)
        return queryset

    def perform_destroy(self, instance):
        instance.delete()
        if instance.is_default and self.get_queryset().exists():
            addr = self.get_queryset().last()
            addr.is_default=True
            addr.save()
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        return super().partial_update(request, *args, **kwargs)
    

class HappyShopOrderInfoViewSet(viewsets.ModelViewSet):
    """订单列表，需要登录
    list:
        订单列表，只可查看自己的订单
    create:
        创建新订单
    update:
        修改订单
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = HappyShopOrderInfoSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        queryset = HappyShopOrderInfo.objects.filter(is_del=False, owner=self.request.user)
        return queryset
    
    def create(self, request, *args, **kwargs):
        """ 重写视图的create方法 """
        """前端传进来的数据格式
        <QueryDict: {
            'address': ['{"id":23,"name":"张真","phone":"17609206698","email":"","province":"省份","city":"城市","county":"区县","address":"详细地址","is_default":true}'], 
            'carts': ['[{"id":33,"num":1,"sku":1,"sku_data":[{"sku_id":1,"spu_id":1,"title":"Apple iPhone 13 Pro (A2639) 128GB 远峰蓝色 支持移动联通电信5G 双卡双待手机",
                "sub_title":"Apple iPhone 13 Pro (A2639) 128GB 远峰蓝色 支持移动联通电信5G 双卡双待手机","options":"64G,蓝色",
                "sell_price":13,"stocks":100,"main_picture":"/HappyShop/sku/cdb86550185fe4b7.jpg","sku_total":"13.00","cart_count":1}]}]'], 
            'pay_method': ['2']}>
        """
        """后端需要的数据格式
        <QueryDict: {'csrfmiddlewaretoken': ['L3oGNK84fFFCYZjFzqUGP6i0ZMEJ2VTttlJ8uPIDLTUNWSVAkPGFJ7VYyP6HwNR0'], 
            'pay_method': ['2'], 
            'total_amount': ['15'], 
            'order_mark': ['购物车结算后清空'], 
            'freight': ['1'], 
            'name': ['学生A'], 
            'phone': ['18391037604'], 
            'email': ['studentA@qq.com'], 
            'address': ['测试']}>
        """
        # 组装后端需要的数据格式data
        data = {}
        team_datas = request.data
        addr_dict = json.loads(team_datas['address'])
        data['pay_method'] = int(team_datas['pay_method'])
        data['total_amount'] = self.get_total_amount(team_datas['carts']).to_eng_string()
        data['freight'] = 0
        data['name'] = addr_dict['name']
        data['phone'] = addr_dict['phone']
        data['email'] = addr_dict['email']
        data['address'] = f"""\
            {addr_dict['province']}\
            {addr_dict['city']}\
            {addr_dict['county']}\
            {addr_dict['address']}\
            """.strip().replace(" ", "")
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        ############ 创建订单时关联创建订单商品 #############
        # 这里的代码是否可以移动到perform_create方法中处理？
        # 到这里 订单就创建成功了，那么需要处理订单关联的商品
        carts_ids = self.get_carts_ids(team_datas['carts'])
        id = serializer.data['id']
        order_sn = serializer.data['order_sn']
        order_info = HappyShopOrderInfo.objects.filter(id=id, order_sn=order_sn, owner=request.user).first()
        # 思考：这里的商品数量应该获取购物车对应的数量，那这里依然应该以购物车为基准
        for cart in self.get_carts(team_datas['carts']):
            sku = HappyShopSKU.objects.get(id=cart['sku'])
            print(sku.sell_price)
            HappyShopOrderSKU.objects.create(order=order_info, sku=sku, count=cart['num'], price=sku.sell_price)
        # 删除已经流转到订单的购物车数据
        HappyShopingCart.objects.filter(id__in=carts_ids).delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def get_total_amount(self, carts):
        total_amount = 0
        # 抱着后端永远不相信前端的编程态度，前端虽然传过来了需要的单价及数量
        # 但我这里还是选择sku的单价去数据库查找计算，不用前端给的值
        for cart in self.get_carts(carts):
            sku = HappyShopSKU.objects.get(id=cart['sku'])
            # 单价从数据库获取，数量从前端获取
            total_amount += cart['num'] * sku.sell_price
        return total_amount

    def get_carts_ids(self, carts):
        # 获取购物车的ids
        carts = self.get_carts(carts)
        cart_ids = [cart['id'] for cart in carts]
        return cart_ids
    
    def get_carts(self, carts):
        # 获取前端传进来的购物车数据
        return json.loads(carts)
    
    def partial_update(self, request, *args, **kwargs):
        # 确认收货
        id = int(kwargs.get('pk'))
        HappyShopOrderInfo.objects.filter(id=id).update(pay_status=4)
        return super().partial_update(request, *args, **kwargs)


class HappyShopPayViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """立即支付
    create:
        创建立即支付订单
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = HappyShopOrderInfoSerializer
    authentication_classes = [SessionAuthentication]

    def create(self, request, *args, **kwargs):
        data = {}
        team_datas = request.data
        addr_dict = json.loads(team_datas['address'])
        sku_list = json.loads(team_datas['sku_data'])
        data['pay_method'] = int(team_datas['pay_method'])
        data['name'] = addr_dict['name']
        data['phone'] = addr_dict['phone']
        data['email'] = addr_dict['email']
        data['address'] = f"""\
            {addr_dict['province']}\
            {addr_dict['city']}\
            {addr_dict['county']}\
            {addr_dict['address']}\
            """.strip().replace(" ", "")
        data['freight'] = 0   # 运费
        sku = HappyShopSKU.objects.get(id=sku_list[0]['sku_id'])
        data['total_amount'] = (int(sku_list[0]['num']) * sku.sell_price).to_eng_string()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # 保存订单关联商品
        id = serializer.data['id']
        order_sn = serializer.data['order_sn']
        order_info = HappyShopOrderInfo.objects.filter(
            id=id, order_sn=order_sn, owner=request.user).first()
        HappyShopOrderSKU.objects.create(
            order=order_info, sku=sku, count=int(sku_list[0]['num']), price=sku.sell_price)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)