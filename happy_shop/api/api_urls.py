from unicodedata import name
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.goods import (
    HappyShopCategoryViewsets, HappyShopBrandViewsets, HappyShopSPUViewsets,
    HappyShopSKUViewsets)

from .views.order import (
    HappyShopingCartViewsets, HappyShopAddressViewsets, HappyShopOrderInfoViewSet, HappyShopPayViewSet)

from .views.base import HappyShopBannerViewsets
from .views.comment import HappyShopRateViewsets

router = DefaultRouter()

# 分类接口
## list        /categories/
## retrieve    /categories/{id}/
router.register('categories', HappyShopCategoryViewsets, basename="categories")

# 品牌接口
router.register('brands', HappyShopBrandViewsets, basename="brands")

# 商品详情接口
router.register('spu_goods', HappyShopSPUViewsets, basename="spu_goods")

# 商品详情接口
router.register('sku_goods', HappyShopSKUViewsets, basename="sku_goods")

# 购物车接口，增删改查
router.register('carts', HappyShopingCartViewsets, basename="carts")

# 收货地址接口
router.register('address', HappyShopAddressViewsets, basename="address")

# 订单接口
router.register('orderinfo', HappyShopOrderInfoViewSet, basename="orderinfo")

# banner接口
router.register('banners', HappyShopBannerViewsets, basename="banners")

# 商品列表页立即支付接口
router.register('paynow', HappyShopPayViewSet, basename="paynow")

# 商品打分接口
router.register('rate', HappyShopRateViewsets, basename="rate")


urlpatterns = router.urls
