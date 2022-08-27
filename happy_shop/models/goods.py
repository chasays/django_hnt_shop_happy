from django.db import models
from django.core.cache import cache

from .models import BaseModelMixin, CarouselModelMixin


class HappyShopCategory(BaseModelMixin):
    """商品分类模型
    """
    name = models.CharField("分类名称", max_length=50)
    desc = models.CharField("分类描述", max_length=100, blank=True, default="")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sub_cates",
        verbose_name="父级分类"
    )
    icon = models.ImageField(
        "分类图标",
        upload_to="happyshop/cateicon/",
        blank=True,
        null=True,
        max_length=200,
        help_text="大小为 96px * 96px")
    is_nav = models.BooleanField("是否为导航", default=False)
    sort = models.PositiveIntegerField("排序", default=0)

    # TODO: Define fields here

    class Meta:
        ordering = ['-sort']
        verbose_name = "商品分类"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.name
    
    @classmethod
    def get_navs(cls):
        """递归菜单,并放到缓存当中

        Returns:
            返回递归生成的菜单数据
        """
        navs = cache.get('navs')
        if navs:
            return navs
        queryset = cls.objects.filter(is_del=False).values(
            'id', 'name', 'parent', 'is_nav', 'icon', 'sort')
        from happy_shop.utils import generate_tree
        navs_tree = generate_tree(list(queryset), None)
        cache.set('navs', navs_tree, 60)
        navs = cache.get('navs')
        return navs


class HappyShopBrand(BaseModelMixin):
    """商品品牌模型
    """
    categories = models.ManyToManyField(
        HappyShopCategory, blank=True, verbose_name="所属分类", related_name="brand_cates", help_text="多对多")
    name = models.CharField("品牌名称", max_length=50)
    desc = models.CharField("品牌描述", max_length=100, blank=True, default="")
    logo = models.ImageField(
        "品牌logo",
        upload_to="happyshop/brand/",
        max_length=200, blank=True, null=True
    )
    sort = models.PositiveIntegerField("排序", default=0)

    class Meta:
        ordering = ['-sort']
        verbose_name = "商品品牌"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.name


class HappyShopSPU(BaseModelMixin):
    """商品SPU
    与淘宝的商品展示模式是一致的，以商品的SPU信息为最终展示页
    一个SPU下边包含多个SKU，SPU的信息是多个SKU的共用信息！
    
    例子：一个苹果手机就是一个SPU，不同颜色配置则是SKU，但商品的
    最终展示形态为SPU，SKU用作唯一库存标记！    
    
    备注：这里的总库存指该SPU下所有SKU的库存总和，总销量指该SPU下所有SKU的销量之和
    
    """
    title = models.CharField("商品标题", max_length=60)
    sub_title = models.CharField("商品副标题", max_length=100)
    desc = models.CharField("商品简介", max_length=150, blank=True, null=True)
    main_picture = models.ImageField("商品主图", upload_to="happyshop/spu/", max_length=200)
    stocks = models.PositiveIntegerField("总库存", default=0)
    sales = models.PositiveIntegerField("总销量", default=0)
    content = models.TextField("商品详情")
    category = models.ManyToManyField(HappyShopCategory, related_name="spu_cates", verbose_name="商品分类")
    brand = models.ForeignKey(HappyShopBrand, on_delete=models.CASCADE, verbose_name="商品品牌")
    is_new = models.BooleanField("是否新品", default=False)
    is_hot = models.BooleanField("是否热销", default=False)
    is_best = models.BooleanField("是否精品", default=False)
    is_shelves = models.BooleanField("是否促销", default=False)
    after_services = models.TextField("售后说明", default="", blank=True)
    sort = models.PositiveIntegerField("排序", default=0)

    class Meta:
        ordering = ['-sort']
        verbose_name = "商品SPU"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.title


class HappyShopSKU(BaseModelMixin):
    """ 商品SKU """
    spu = models.ForeignKey(HappyShopSPU, on_delete=models.CASCADE, related_name="skus", verbose_name="商品")
    options = models.ManyToManyField('HappyShopSPUSpecOption', blank=True, verbose_name="规格值")
    main_picture = models.ImageField(
        "商品主图", upload_to="happyshop/sku/", max_length=200)
    bar_code = models.CharField("商品条码", max_length=50, default="", blank=True)
    sell_price = models.DecimalField("商品售价", max_digits=12, decimal_places=2)
    market_price = models.DecimalField("市场价/划线价", max_digits=12, decimal_places=2)
    cost_price = models.DecimalField("成本价", max_digits=12, decimal_places=2)
    stocks = models.PositiveIntegerField("库存", default=0)
    sales = models.PositiveIntegerField("销量", default=0)
    sort = models.PositiveIntegerField("排序", default=0)

    class Meta:
        ordering = ['-sort']
        verbose_name = "商品SKU"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return f'{self.spu.title} {list(self.options.values_list("value", flat=True))}'
    
    @property
    def get_options(self):
        """ 获取该商品的规格值列表
        return (_type_.list) 
        """
        return list(self.options.values_list("value", flat=True))


class HappyShopSPUSpec(BaseModelMixin):
    """ 商品规格选项 """
    
    name = models.CharField("规格名称", max_length=50)
    
    class Meta:
        ordering = ['-add_date']
        verbose_name = "商品规格"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.name
    

class HappyShopSPUSpecOption(BaseModelMixin):
    """商品的规格值
        SKU将与这个表建立一对多的关联关系
        一个SKU可以有多个规格值
        例如：一件衣服拥有颜色 和 大小等多个规格值
    """
    spec = models.ForeignKey(HappyShopSPUSpec, on_delete=models.CASCADE, related_name="specs", verbose_name="规格")
    value = models.CharField("规格值", max_length=50)

    class Meta:
        ordering = ['-add_date']
        verbose_name = "商品规格值"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.value
    

class HappyShopSpecToOption(BaseModelMixin):
    """商品规格的关系表
    
        多个SPU下可以有多个规格
        多个规格可以同时归属于多个SPU
        
        比如衣服的颜色为规格，那么他的规格值就包含 红色  绿色 粉色多种颜色
        那不同的衣服的spu可能都有颜色这个规格，那么就可以一次性设置
    
    """
    spu = models.ManyToManyField(
        HappyShopSPU,
        related_name="specs_options",
        blank=True,
        verbose_name="商品SPUS"
    )
    spec = models.ManyToManyField(HappyShopSPUSpec, verbose_name="规格")
    
    class Meta:
        ordering = ['-add_date']
        verbose_name = "商品规格关系"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return f"{self.spu.values_list('id', flat=True)}=>{self.spec.values_list('name', flat=True)}"


class HappyShopSPUCarousel(CarouselModelMixin):
    """ 商品轮播图 """
    spu = models.ForeignKey(
        HappyShopSPU, 
        related_name="carousel",
        on_delete=models.CASCADE,
        verbose_name="商品"
    )
    
    class Meta:
        verbose_name = "商品轮播图"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return f'{self.spu.title}的轮播图{self.img}'
