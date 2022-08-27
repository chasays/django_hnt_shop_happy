from rest_framework import viewsets
from rest_framework import mixins
from happy_shop.models import HappyShopBanner
from happy_shop.api.serializers.base import HappyShopBannerSerializer


class HappyShopBannerViewsets(mixins.ListModelMixin, viewsets.GenericViewSet):
    """banner视图
    list:
        banner列表
    """
    serializer_class = HappyShopBannerSerializer

    def get_queryset(self):
        return HappyShopBanner.objects.filter(is_del=False)