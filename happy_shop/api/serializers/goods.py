from rest_framework import serializers

from happy_shop.models import (
    HappyShopCategory, HappyShopBrand, HappyShopSPU,
    HappyShopSKU, HappyShopSpecToOption, HappyShopSPUSpec, HappyShopSPUSpecOption,
    HappyShopSPUCarousel)


class HappyShopeCategorySerializer(serializers.ModelSerializer):
    """HappyShopCategory 的序列化器
    """
    sub_cates = serializers.SerializerMethodField()
    brand_cates = serializers.StringRelatedField(many=True)

    class Meta:
        model = HappyShopCategory
        fields = ('id', 'name', 'desc', 'parent', 'sub_cates', 'brand_cates', 'icon', 'is_nav', 'sort')

    def get_sub_cates(self, obj):
        """序列化自关联子类

        Args:
            obj (当前模型实例): 模型实例对象

        Returns:
            _serializers_: 返回包含子类的序列化器
        """
        if obj.sub_cates:
            return HappyShopeCategorySerializer(obj.sub_cates, many=True).data
        else:
            return None


class SpuToSkuSerializer(serializers.ModelSerializer):
    """ Spu中所有的SKU 序列化器
    """
    options = serializers.StringRelatedField(many=True)

    class Meta:
        model = HappyShopSKU
        fields = '__all__'


class HappyShopSPUSpecOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = HappyShopSPUSpecOption
        fields = ('id', 'value', 'specs')


class HappyShopSPUSpecSerializer(serializers.ModelSerializer):
    """HappyShopSpec 序列化器
    """
    specs = serializers.StringRelatedField(many=True)

    class Meta:
        model = HappyShopSPUSpec
        fields = ('id', 'name', 'specs')


class HappyShopSpecToOptionSerializer(serializers.ModelSerializer):
    """HappyShopSpecToOption 序列化器
    """
    spec = HappyShopSPUSpecSerializer(many=True)

    class Meta:
        model = HappyShopSpecToOption
        fields = ['spec']


class HappyShopSPUCarouselSerializer(serializers.ModelSerializer):
    """HappyShopSPUCarousel 序列化器
    """
    class Meta:
        model = HappyShopSPUCarousel
        fields = '__all__'


class HappyShopSPUSerializer(serializers.ModelSerializer):
    """ SPU 序列化器
    """
    skus = SpuToSkuSerializer(many=True)
    specs = serializers.SerializerMethodField()
    # specs_options = HappyShopSpecToOptionSerializer(many=True)
    # carousel = HappyShopSPUCarouselSerializer(many=True)
    carousel = serializers.SerializerMethodField()

    class Meta:
        model = HappyShopSPU
        fields = '__all__'
    
    def get_specs(self, obj):
        specs = obj.specs_options.filter(is_del=False)
        datas = HappyShopSpecToOptionSerializer(specs, many=True).data
        specs = []
        if datas:
            ops = datas[0].get('spec')
            for op in ops:
                specs.append(op)
        return specs

    def get_carousel(self, obj):
        carousel = obj.carousel.filter(is_del=False)
        datas = HappyShopSPUCarouselSerializer(carousel, many=True).data
        datas.insert(0,{
            "img": obj.main_picture.url
        })
        return datas

class HappyShopSKUSerializer(serializers.ModelSerializer):
    """ SKU 序列化器
    """
    spu = HappyShopSPUSerializer(many=False)
    options = serializers.StringRelatedField(many=True)

    class Meta:
        model = HappyShopSKU
        fields = '__all__'


class HappyShopeCategoryDetailSerializer(serializers.ModelSerializer):

    """HappyShopCategory 的详情序列化器
    """
    spu_cates = HappyShopSPUSerializer(many=True)  # 当前分类下的所有spu
    skus = serializers.SerializerMethodField()      # 当前分类下的所有sku

    class Meta:
        model = HappyShopCategory
        fields = ('id', 'name', 'desc', 'parent', 'sub_cates','skus', 'spu_cates', 'brand_cates', 'icon', 'is_nav', 'sort', )

    def get_skus(self, obj):
        # 返回当前分类下的所有SKU
        spus = obj.spu_cates.filter(is_del=False)
        skus_id = []
        for spu in spus:
            skus_id += list(spu.skus.values_list('id', flat=True))
        queryset = HappyShopSKU.objects.filter(id__in=skus_id, is_del=False)
        return HappyShopSKUSerializer(queryset, many=True).data


class HappyShopBrandSerializer(serializers.ModelSerializer):
    
    """HappyShopBrand 序列化器
    """
    categories = HappyShopeCategorySerializer(many=True)
    
    class Meta:
        model = HappyShopBrand
        fields = ('categories', 'name', 'desc', 'logo', 'sort',)
    

