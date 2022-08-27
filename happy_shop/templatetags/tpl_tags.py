from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from happy_shop.pay.alipay import alipay
from happy_shop.models import HappyShopCategory, HappyShopOrderInfo
from happy_shop.conf import happy_shop_settings
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_navs():
    """ 获取菜单数据 """
    return HappyShopCategory.get_navs()


@register.simple_tag
def alipay_url(order_sn):
    # 模板中传入订单号即可快速跳转到支付宝支付地址
    # 快捷支付方式
    order = HappyShopOrderInfo.objects.get(order_sn=order_sn)
    if order.pay_status == 1:
        url = alipay.api_alipay_trade_page_pay(
            subject=order.order_sn,
            out_trade_no=order.order_sn,
            total_amount=order.total_amount.to_eng_string(),
            return_url=happy_shop_settings.ALIPAY.get('RETURN_URL'),
            # 可选, 不填则使用默认notify url
            notify_url=happy_shop_settings.ALIPAY.get('NOTIFY_URL')     
        )
        if settings.DEBUG:
            re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(
                data=url)
        else:
            re_url = "https://openapi.alipay.com/gateway.do?{data}".format(
                data=url)
    return re_url
