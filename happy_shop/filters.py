from dataclasses import fields
import django_filters
from happy_shop.models import HappyShopCategory, HappyShopSPU, HappyShopSKU, HappyShopBrand


class HappyShopSPUFilter(django_filters.FilterSet):

    order = django_filters.OrderingFilter(fields=('skus__sell_price',))

    class Meta:
        model = HappyShopSPU
        fields = ['brand', 'is_new', 'is_hot', 'is_best', 'is_shelves']


class HappyShopSKUFilter(django_filters.FilterSet):
    """商品分类页筛选
    """
    order = django_filters.OrderingFilter(fields=('sell_price',), label='排序', field_labels={'sell_price':'售价'},)
    spu__brand = django_filters.ModelChoiceFilter(field_name='spu__brand', queryset=HappyShopBrand.objects.filter(is_del=False), label="品牌")
    spu__is_new = django_filters.BooleanFilter(field_name='spu__is_new', label="是否新品")
    spu__is_best = django_filters.BooleanFilter(field_name='spu__is_best', label="是否精品")
    spu__is_hot = django_filters.BooleanFilter(field_name='spu__is_hot', label="是否热销")
    spu__is_shelves = django_filters.BooleanFilter(field_name='spu__is_shelves', label="是否促销")
    spu__category = django_filters.ModelChoiceFilter(
        field_name='spu__category', 
        queryset=HappyShopCategory.objects.filter(parent__isnull=False, is_del=False), 
        label="分类",)
    
    class Meta:
        model = HappyShopSKU
        fields = ['spu__brand','spu__category', 'spu__is_new', 
                  'spu__is_hot', 'spu__is_best', 'spu__is_shelves']
