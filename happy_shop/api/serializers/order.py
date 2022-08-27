import time
from django.conf import settings
from rest_framework import serializers
from happy_shop.pay import alipay
from happy_shop.conf import happy_shop_settings

from happy_shop.models import (
    HappyShopingCart, HappyShopAddress, HappyShopOrderInfo,
    HappyShopOrderSKU)


class HappyShopingCartSerializer(serializers.ModelSerializer):
    """ 购物车数据序列化 """

    # owner = serializers.HiddenField(
    #     default = serializers.CurrentUserDefault())
    sku_data = serializers.SerializerMethodField()

    class Meta:
        model = HappyShopingCart
        fields = ("id", "num", "sku", "sku_data")

    def get_sku_data(self, obj):
        sku = obj.sku
        cart_count = HappyShopingCart.objects.filter(owner=obj.owner).count()
        return [{
            "sku_id": sku.id,
            "spu_id": sku.spu.id,
            "title": sku.spu.title,
            "sub_title": sku.spu.sub_title,
            "options": ",".join(sku.get_options),
            "sell_price": sku.sell_price,
            "stocks": sku.stocks,
            "main_picture": sku.main_picture.url,
            "sku_total": sku.sell_price * obj.num,
            "cart_count": cart_count
        }]

    def create(self, validated_data):
        """ 重写create """

        validated_data['owner'] = self.context["request"].user

        """ 判断该SKU是否已被加入购物车，重复加入只修改商品数量，不增加新的购物车
        这里直接return出去carts应该也是可以的，但为了不出bug我在视图中重写了create方法
        carts = HappyShopingCart.objects.filter(owner=self.context["request"].user, sku=validated_data['sku'])
        if carts.exists():
            instance = carts.first()
            instance.num += validated_data['num']
            instance.save()
            return carts
        """
        return super().create(validated_data)


class HappyShopAddressSerializer(serializers.ModelSerializer):
    """ 收货地址序列化 """

    owner = serializers.HiddenField(
        default = serializers.CurrentUserDefault())

    class Meta:
        model = HappyShopAddress
        fields = ('id', 'owner', 'name', 'phone', 'email', 'province', 'city', 'county', 'address', 'is_default', )

    def create(self, validated_data):
        """ 默认收货地址只能有一个
        如果用户新增要设置为默认地址，那么把其他地址的默认标识改为False
        """
        is_default = validated_data['is_default']
        if is_default:
            address = HappyShopAddress.objects.filter(is_default=True, owner=self.context["request"].user)
            if address.exists:
                address.update(is_default=False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """ 设为默认值 """
        if instance.is_default:
            address = HappyShopAddress.objects.filter(is_default=True, owner=self.context["request"].user)
            if address.exists:
                address.update(is_default=False)
        return super().update(instance, validated_data)

    
class HappyShopOrderInfoSerializer(serializers.ModelSerializer):
    """订单序列化
    """
    owner = serializers.HiddenField(
        default = serializers.CurrentUserDefault())
    order_sn = serializers.CharField(read_only=True)
    trade_sn = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    # 支付宝返回的url
    alipay_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = HappyShopOrderInfo
        # fields = "__all__"
        exclude = ('is_del',)
    
    def get_alipay_url(self, obj):
        """
        支付宝支付地址
        """
        # url = alipay.client_api(
        #     "alipay.trade.page.pay",
        #     biz_content={
        #         "subject": obj.order_sn,
        #         "out_trade_no": obj.order_sn,
        #         "total_amount": obj.total_amount.to_eng_string(),
        #     }
        # )
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=obj.order_sn,
            total_amount=obj.total_amount.to_eng_string(),
            subject=obj.order_sn,
            return_url = happy_shop_settings.ALIPAY.get('RETURN_URL'),
            notify_url=happy_shop_settings.ALIPAY.get('NOTIFY_URL')     # 可选, 不填则使用默认notify url
        )
        if settings.DEBUG:
            re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=order_string)
        else:
            re_url = "https://openapi.alipay.com/gateway.do?{data}".format(data=order_string)
        return re_url
    
    def generate_order_sn(self):
        # 当前时间 + userid + 随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{user_id}{ranstr}".format(
            time_str = time.strftime("%Y%m%d%H%M%S"),
            user_id = self.context["request"].user.id,
            ranstr = random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        # 设置order_sn的值
        attrs["order_sn"] = self.generate_order_sn()
        return attrs
    