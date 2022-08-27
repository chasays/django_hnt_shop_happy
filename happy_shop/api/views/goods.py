from rest_framework import viewsets
from rest_framework import mixins
# from django_filters import rest_framework as filters
from rest_framework import filters  # 筛选
from django_filters.rest_framework import DjangoFilterBackend  # 过滤
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from happy_shop.models import (
    HappyShopCategory, HappyShopBrand, HappyShopSPU, HappyShopSKU
)
from happy_shop.api.serializers.goods import (
    HappyShopeCategorySerializer, HappyShopBrandSerializer, HappyShopeCategoryDetailSerializer,
    HappyShopSPUSerializer, HappyShopSKUSerializer
)

from ..pagination import HappyShopSKUPagination
from ..filters import (
    HappyShopSKUFilter, HappyShopSPUFilter, HappyShopCategoryFilter
)
class HappyShopCategoryViewsets(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    """
    分类列表视图，返回所有的商品列表数据
    list:
        商品分类列表数据
    """
   
    # filter_backends = [MyFilterBackend]
    filterset_class = HappyShopCategoryFilter

    def get_serializer_class(self):
        """ 动态序列化 """
        if self.action == "list":
            return HappyShopeCategorySerializer
        elif self.action == "retrieve":
            return HappyShopeCategoryDetailSerializer
        return HappyShopeCategorySerializer
    
    def get_queryset(self):
        """ 根据不同的请求返回不同的数据 """
        cates_queryset = HappyShopCategory.objects.filter(is_del=False, parent__isnull=True)
        if self.action == "list":
            return cates_queryset
        elif self.action == "retrieve":
            return HappyShopCategory.objects.filter(is_del=False)
        return cates_queryset


class HappyShopBrandViewsets(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ HappyShopBrand 商品品牌接口

    list:
        @params mixins.ListModelMixin
        返回商品品牌列表
    retrieve:
        @params mixins.RetrieveModelMixin
        返回商品品牌详情
    """
    queryset = HappyShopBrand.objects.filter(is_del=False)
    serializer_class = HappyShopBrandSerializer


class HappyShopSPUViewsets(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ SPU  
    spu可以全局缓存，因为不影响库存
    """
    queryset = HappyShopSPU.objects.filter(is_del=False)
    serializer_class = HappyShopSPUSerializer
    filterset_class = HappyShopSPUFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("title", "sub_title")
    ordering_fields = ('skus__sell_price',)


class HappyShopSKUViewsets(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ SKU  
    sku则不能全局缓存，因为库存会实时变动，需要更精细化控制
    """
    queryset = HappyShopSKU.objects.filter(is_del=False)
    serializer_class = HappyShopSKUSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = HappyShopSKUFilter
    pagination_class = HappyShopSKUPagination
    search_fields = ("spu__title", "spu__sub_title")
    ordering_fields = ('sell_price', 'sales', 'sort')