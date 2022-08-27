from rest_framework import serializers
from happy_shop.models import HappyShopBanner


class HappyShopBannerSerializer(serializers.ModelSerializer):
    """
    Banner Serializer
    """
    class Meta:
        model = HappyShopBanner
        fields = "__all__"