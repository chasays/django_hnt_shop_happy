from rest_framework import serializers
from ...models import HappyShopRate, HappyShopOrderSKU


class HappyShopRateSerializer(serializers.ModelSerializer):
    """
    HappyShopRate Serializer
    """
    owner = serializers.HiddenField(
        default = serializers.CurrentUserDefault())
    
    class Meta:
        model = HappyShopRate
        # fields = "__all__"
        exclude = ("content_type", )