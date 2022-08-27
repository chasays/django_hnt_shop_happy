from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join
from happy_shop.admin.admin import happy_shop_site
# Register your models here.
from .widget import WangEditorWidget
from ..models import (
    HappyShopCategory, HappyShopBrand, HappyShopSPU,
    HappyShopSKU, HappyShopSPUSpec, HappyShopSpecToOption,
    HappyShopSPUSpecOption, HappyShopSPUCarousel, HappyShopingCart, HappyShopOrderInfo,
    HappyShopOrderSKU, HappyShopBanner, HappyShopRate
)

# admin.site.register(HappyShopRate)
# admin.site.register(HappyShopOrderSKU)

class HappyShopAdmin(admin.ModelAdmin):
    '''Admin View for '''
    exclude = ('is_del',)


class HappyShopSKUAdmin(admin.TabularInline):
    '''Admin View for HappyShopSKU'''
    model = HappyShopSKU
    extra = 2
    min_num = 1
    exclude = ('is_del', 'sales', 'sort')


class HappyShopSPUCarouselInlineAdmin(admin.TabularInline):
    model = HappyShopSPUCarousel
    extra = 1
    exclude = ('is_del', 'target_url', 'img_url')

# @admin.register(HappyShopCategory, site=happy_shop_site)
@admin.register(HappyShopCategory)
class HappyShopCategoryAdmin(HappyShopAdmin):
    '''Admin View for HappyShopCategory'''

    list_display = ('name', 'is_icon',  'parent', 'is_nav', 'sort', 'add_date')
    list_filter = ('parent',)
    list_editable = ('is_nav', 'sort')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 父类只能选择顶级
        if db_field.name == 'parent':
            kwargs["queryset"] = HappyShopCategory.objects.filter(
                parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description="分类图标")
    def is_icon(self, obj):
        if obj.icon:
            return format_html(f'<img src="{obj.icon.url}" width="32px" height="32px" />')

# @admin.register(HappyShopBrand, site=happy_shop_site)
@admin.register(HappyShopBrand)
class HappyShopBrandAdmin(HappyShopAdmin):
    '''Admin View for HappyShopCategory'''
    list_display = ('name', 'is_logo', 'sort', 'add_date')
    list_editable = ('sort',)

    @admin.display(description="品牌图标")
    def is_logo(self, obj):
        if obj.logo:
            return format_html(f'<img src="{obj.logo.url}" width="32px" height="32px" />')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # 归属分类只能二级
        if db_field.name == 'categories':
            kwargs['queryset'] = HappyShopCategory.objects.filter(
                parent__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# @admin.register(HappyShopSPU, site=happy_shop_site)
@admin.register(HappyShopSPU)
class HappyShopSPUAdmin(HappyShopAdmin):
    '''Admin View for HappyShopSPU'''
    list_display = ('get_title', 'get_main_picture',
                    'get_category', 'brand', 'is_new', 'sort', 'add_date')
    list_editable = ('sort',)
    exclude = ('is_del', 'stocks', 'sales', 'sort')
    readonly_fields = ('get_main_picture', )
    inlines = [HappyShopSPUCarouselInlineAdmin, HappyShopSKUAdmin]
    
    formfield_overrides = {
        models.TextField: {'widget': WangEditorWidget},
    }

    @admin.display(description="标题")
    def get_title(self, obj):
        if obj.title:
            return format_html(f'{obj.title[:30]}...')

    @admin.display(description="商品图")
    def get_main_picture(self, obj):
        if obj.main_picture:
            return format_html(f'<img src="{obj.main_picture.url}" width="32px" height="32px" />')

    @admin.display(description="所属分类")
    def get_category(self, obj):
        if obj.category:
            return format_html_join(
                mark_safe(','),
                '{}',
                ((line,) for line in obj.category.all()),
            ) or mark_safe("<span class='errors'>I can't determine this category.</span>")

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # 归属分类只能二级
        if db_field.name == 'category':
            kwargs['queryset'] = HappyShopCategory.objects.filter(
                parent__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # class Media:
    #     js = (
    #         'admin/js/vendor/jquery/jquery.min.js',
    #         'https://cdn.jsdelivr.net/npm/wangeditor@latest/dist/wangEditor.min.js',
    #         'happy_shop/js/weditor.js'
    #     )

# @admin.register(HappyShopSpecToOption, site=happy_shop_site)
@admin.register(HappyShopSpecToOption)
class HappyShopSpecToOptionAdmin(HappyShopAdmin):
    '''Admin View for HappyShopSpecToOption'''
    list_display = ('get_spu', 'get_spec')
    # list_editable = ('sort',)

    @admin.display(description="商品")
    def get_spu(self, obj):
        if obj.spu:
            return format_html_join(
                mark_safe('<br>'),
                '{}',
                ((line,) for line in obj.spu.all()),
            ) or mark_safe("<span class='errors'>I can't determine this category.</span>")

    @admin.display(description="规格")
    def get_spec(self, obj):
        if obj.spec:
            return format_html_join(
                mark_safe(','),
                '{}',
                ((line,) for line in obj.spec.all()),
            ) or mark_safe("<span class='errors'>I can't determine this category.</span>")


class HappyShopSPUSpecOptionInlineAdmin(admin.TabularInline):
    model = HappyShopSPUSpecOption
    extra = 1
    exclude = ('is_del',)


# @admin.register(HappyShopSPUSpec, site=happy_shop_site)
@admin.register(HappyShopSPUSpec)
class HappyShopSPUSpecAdmin(HappyShopAdmin):
    '''Admin View for HappyShopSPUSpec'''
    list_display = ('name', 'add_date')
    inlines = [
        HappyShopSPUSpecOptionInlineAdmin
    ]


# @admin.register(HappyShopBanner, site=happy_shop_site)
@admin.register(HappyShopBanner)
class HappyShopBannerAdmin(HappyShopAdmin):
    '''Admin View for HappyShopBanner'''
    list_display = ('get_img', 'target_url', 'sort', 'add_date')

    @admin.display(description="轮播图")
    def get_img(self, obj):
        if obj.img:
            return format_html(f'<img src="{obj.img.url}" width="auto" height="100px" />')


# @admin.register(HappyShopOrderInfo, site=happy_shop_site)
@admin.register(HappyShopOrderInfo)
class HappyShopOrderInfoAdmin(HappyShopAdmin):
    '''Admin View for '''

    list_display = ('id', 'owner', 'order_sn', 'pay_status', 'pay_method',
                    'order_product', 'total_amount', 'freight', 'pay_time', )
    list_editable = ('pay_status',)
    list_display_links = ('order_sn',)
    readonly_fields = ('pay_time', 'owner', 'trade_sn')

    @admin.display(description="订单商品")
    def order_product(self, obj):
        product_queryset = obj.happyshopordersku_set.all()
        product_list = []
        for product in product_queryset:
            product_list.append('''
                <div style="float:left; width:50px; height: 50px; margin-right:5px">
                    <img src="{}" width="50" height="50" />
                </div> 
                '''.format(product.sku.main_picture.url))
            product_list.append(
                f'<div style="font-weight: 500;">{product.sku.spu.title}</div>')
            product_list.append(
                f'<div style="color:red">数量：{str(product.count)}</div>')
            product_list.append("规格：{}".format(
                ','.join(product.sku.get_options)))
            product_list.append('<div style="clear:both"></div>')
        return mark_safe(''.join(product_list))

    def has_add_permission(self, request) -> bool:
        return False
