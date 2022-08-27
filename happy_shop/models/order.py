from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .models import BaseModelMixin
from .goods import HappyShopSKU

User = get_user_model()


class HappyShopOrderInfo(BaseModelMixin):
    """订单信息"""

    class PayMethodChoices(models.IntegerChoices):
        CASH = 1, _('货到付款')
        ALIPAY = 2, _('支付宝')
        WECHATPAY = 3, _('微信支付')
        OVERPAY = 4, _('余额支付')

    class OrderStatusChoices(models.IntegerChoices):
        TOBPAY = 1, _('待支付')
        TOBDELIVER = 2, _('待发货')
        TOBRECEIVED = 3, _('待收货')
        TOBEVALUATE = 4, _('待评价')
        COMPLETE = 5, _('已完成')
        CANCELLED = 6, _('已取消')

    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    order_sn = models.CharField(
        blank=True, default="",
        unique=True, max_length=32,
        verbose_name="订单号", help_text="订单号")
    trade_sn = models.CharField(
        blank=True, null=True,
        unique=True, max_length=64,
        verbose_name="交易号", help_text="交易号")
    pay_status = models.IntegerField(
        choices=OrderStatusChoices.choices, default=1, verbose_name="支付状态", help_text="支付状态")
    pay_method = models.IntegerField(
        choices=PayMethodChoices.choices, default=2, verbose_name="支付方式", help_text="支付方式")
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="商品总金额")
    order_mark = models.CharField(
        blank=True, default="", max_length=100, verbose_name="订单备注", help_text="订单备注")
    freight = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="运费")
    name = models.CharField("签收人", max_length=50, default="")
    phone = models.CharField("手机号", max_length=11, default="")
    email = models.EmailField("邮箱", blank=True, default="", max_length=50)
    address = models.CharField("地址", max_length=150)
    pay_time = models.DateTimeField(
        null=True, blank=True, verbose_name="支付时间", help_text="支付时间")

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn

    @classmethod
    def get_pay_method(cls):
        # 支付方式列表字典
        return dict(cls.PayMethodChoices.choices)

    @classmethod
    def get_pay_default(cls):
        # 获取支付方式的默认值
        return cls._meta.get_field('pay_method').default


class HappyShopOrderSKU(BaseModelMixin):
    """订单商品"""
    order = models.ForeignKey(HappyShopOrderInfo, on_delete = models.PROTECT, verbose_name="订单")
    sku = models.ForeignKey(HappyShopSKU, on_delete = models.PROTECT, blank=True, null=True, verbose_name="订单商品")
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField('单价', max_digits=18, decimal_places=2)
    is_commented = models.BooleanField(default=False, verbose_name="是否已评价")

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.sku.spu.title


class HappyShopAddress(BaseModelMixin):
    """收货地址
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    name = models.CharField("签收人", max_length=50)
    phone = models.CharField("手机号", max_length=11)
    email = models.EmailField("邮箱", blank=True, default="", max_length=50)
    province = models.CharField(max_length=150, verbose_name="省")
    city = models.CharField(max_length=150, verbose_name="市")
    county = models.CharField(max_length=150, verbose_name="区/县")
    address = models.CharField(max_length=150, verbose_name="详细地址")
    is_default = models.BooleanField(default=False, verbose_name="设为默认")
    
    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name
        constraints = [
            # 默认地址唯一约束
            models.UniqueConstraint(fields=('id', 'is_default'), name="unique_happy_addr")
        ]

    def __str__(self):
        return f'{self.name} {self.address}'
    
    @classmethod
    def get_default(cls, user, is_default=True):
        """[获取默认收货地址]

        Args:
            user (request.user): 当前登录用户对象

        Returns:
            [Queryset]: 所属用户的默认收货地址的queryset数据
        """
        return cls.objects.filter(owner=user, is_default=is_default)


class HappyShopingCart(BaseModelMixin):
    # 购物车数据模型
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    sku = models.ForeignKey(HappyShopSKU, on_delete=models.CASCADE, verbose_name="商品sku")
    num = models.PositiveIntegerField(default=1, verbose_name="数量")
    
    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['owner', 'sku'], name='unique_owner_sku_happy')
        ]
        
    def __str__(self):
        return f'{self.owner}{self.sku}'
    
    @classmethod
    def get_cart_count(cls, user):
        # 当前用户的购物车数量
        return cls.objects.filter(owner=user).count()
