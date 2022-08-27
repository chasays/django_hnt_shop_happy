from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from happy_shop.pay import alipay
from happy_shop.models.order import HappyShopOrderInfo


class AliPayView(APIView):
    """ 支付宝支付回调 """

    renderer_classes = [TemplateHTMLRenderer]  # 指定渲染器
    template_name = 'happy_shop/pay_success.html'        # 指定模板
    
    def get(self, request, format=None):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        #  /shop/api/alipay/?charset=utf-8&out_trade_no=20220329093626148&method=alipay.trade.page.pay.return&total_amount=28.00&sign=NLZhXyV7FooSiqoiCcHL52AZfKqU55r1mhGgj1S%2Bz%2Fd1RleVzdKv59BBQBKXT3dEymt311BdVCJaN1aHWNQ7YjZyNRwuoaP8ErUbmf55VT7lioHzDm78klpaxYdgWi3Azm9U4TqpapShI04tTIh9XmvQnQCZqy0ZRwCQtbJoykJKWUa3W3lOEUzVdkSgadH7z0RdGZ2HYR5p9B01XmRmwUBVYIpuyUDmo1qOdjHZ2YnpFVmDxwzGAd7fQlTsxkL6WGJFdYC731Vwiu2SX9ovM894qohdcUV8U3TcfRETK6C3JB8RC6rFsKXirzMRSpUCgeUCKJCEAJYQEIfxK6vF9w%3D%3D&trade_no=2022032922001425410502127353&auth_app_id=2021000116697536&version=1.0&app_id=2021000116697536&sign_type=RSA2&seller_id=2088621955134594&timestamp=2022-03-29+09%3A39%3A09
        data = {}
        data_querydict = request.query_params
        for key, value in data_querydict.items():
            data[key] = value
        signature = data.pop("sign")
        success = alipay.verify(data, signature)
        print(success)
        if success:
            order_sn = data.get('out_trade_no')
            trade_no = data.get('trade_no')
            trade_status = data.get('trade_status')
            print(trade_status)
            order_info = HappyShopOrderInfo.objects.filter(order_sn=order_sn)
            if order_info.exists():
                order = order_info.first()
                order.pay_status = 2
                order.trade_sn = trade_no
                """
                # https://docs.djangoproject.com/zh-hans/4.0/topics/i18n/timezones/#concepts
                # 如果setings配置文件中USE_TZ = True请使用timezone.now()获取当前时间
                反之，使用以下方式，这样代码就会有很好地兼容行，建议使用第一种
                    import datetime
                    now = datetime.datetime.now()
                """
                order.pay_time = timezone.now()
                order.save()
            data['order_id'] = order.id
        return Response({'query_dict': data})

    def post(self, request, format=None):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        data = {}
        data_querydict = request.data
        for key, value in data_querydict.items():
            data[key] = value
        signature = data.pop("sign")
        success = alipay.verify(data, signature)
        if success:
            order_sn = data.get('out_trade_no')
            trade_no = data.get('trade_no')
            trade_status = data.get('trade_status')
            print(trade_status)
            order_info = HappyShopOrderInfo.objects.filter(order_sn=order_sn)
            if order_info.exists():
                order = order_info.first()
                order.pay_status = 2
                order.trade_sn = trade_no
                order.pay_time = timezone.now()
                order.save()
        return Response('success')
