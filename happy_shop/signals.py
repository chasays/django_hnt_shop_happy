from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HappyShopOrderSKU


@receiver(post_save, sender=HappyShopOrderSKU)
def create_ordersku(sender, instance=None, created=False, **kwargs):
    # 订单关联商品保存时减库存加销量
    if created:
        instance.sku.stocks -= instance.count
        instance.sku.sales += instance.count
        instance.sku.save()
