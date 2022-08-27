import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView
from django.core.cache import cache

from happy_shop.conf import happy_shop_settings
from .views import HappyShopLoginRequiredMixin
from happy_shop.models import (
    HappyShopOrderInfo, HappyShopAddress, HappyShopSKU, HappyShopOrderSKU)
from .views import BaseView


class HappyShopingCartView(HappyShopLoginRequiredMixin, BaseView, TemplateView):
    """ 购物车页面 """
    
    template_name = "happy_shop/cart.html"


class HappyShopUserProfileView(HappyShopLoginRequiredMixin, BaseView, TemplateView):
    """ 用户中心 """
    
    template_name = "happy_shop/user_profile.html"


class HappyShopUserOrdersView(HappyShopLoginRequiredMixin, BaseView, ListView):
    """ 我的订单 """
    template_name = "happy_shop/user_orders.html"
    paginate_by = happy_shop_settings.ORDERS_NUM

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.get_queryset()
        context['tobpay_orders'] = self.get_order_status(1)        # 待支付
        context['tobdeliver_orders'] = self.get_order_status(2)    # 待发货
        context['tobreceived_orders'] = self.get_order_status(3)   # 待收货
        context['tobevaluate_orders'] = self.get_order_status(4)   # 待评价
        context['complete_orders'] = self.get_order_status(5)      # 已完成
        context['cancelled_orders'] = self.get_order_status(6)     # 已取消
        return context

    def get_queryset(self):
        return HappyShopOrderInfo.objects.filter(is_del=False, owner=self.request.user).order_by('-add_date')
    
    def get_order_status(self, status):
        queryset = self.get_queryset().filter(pay_status=status)
        return queryset

class HappyShopUserOrdersDetailView(LoginRequiredMixin, BaseView, DetailView):
    """ 订单详情 """
    login_url = 'happy_shop:login'
    redirect_field_name = 'redirect_to'
    template_name = "happy_shop/user_orders_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return HappyShopOrderInfo.objects.filter(is_del=False, owner=self.request.user)


class HappyShopUserAddressView(HappyShopUserProfileView):
    """ 
    收货地址管理 
    """
    template_name = "happy_shop/user_address.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = HappyShopAddress.objects.filter(is_del=False, owner=self.request.user)
        return context


class HappyShopPayView(HappyShopingCartView):
    """ 立即支付界面 """
    template_name = "happy_shop/pay.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sku_data'] = self.get_cache_sku()
        return context

    def get_cache_sku(self):
        """ 
        点击立即购买后缓存当前SKU
        sku_id 
            前端传过来的sku的id值
        return
            sku_id存在返回缓存中的数据
            sku_id不存在返回一个空列表
        """
        sku_id = self.request.GET.get('sku_id')
        num = self.request.GET.get('num')
        if sku_id is None:
            return []
        if sku_id:
            key = f"{self.request.user.username}{sku_id}{num}"
            sku = cache.get(key)
            if not sku:
                skus = []
                for good in HappyShopSKU.objects.filter(id=int(sku_id)):
                    sku_data = {}
                    sku_data['sku_id'] = sku_id
                    sku_data['spu_id'] = good.spu.id
                    sku_data['title'] = good.spu.title
                    sku_data['sub_title'] = good.spu.sub_title
                    sku_data['options'] = ','.join(good.get_options)
                    sku_data['sell_price'] = good.sell_price.to_eng_string()
                    sku_data['stocks'] = good.stocks
                    sku_data['main_picture'] = good.main_picture.url
                    sku_data['sku_total'] = (good.sell_price * int(num)).to_eng_string()
                    sku_data['num'] = num
                    skus.append(sku_data)
                cache.set(key, skus, 3600)
                sku = cache.get(key)
            return json.dumps(sku, ensure_ascii=False)
        
        
class HappyShopOrderSKUDetailView(LoginRequiredMixin, BaseView, DetailView):
    
    template_name = "happy_shop/order_sku_detail.html"
    context_object_name = "order_sku"
    
    def get_queryset(self):
        qs = HappyShopOrderSKU.objects.filter(order__owner=self.request.user)
        return qs
    