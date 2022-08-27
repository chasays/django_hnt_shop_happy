from django.db import models

# Create your models here.

class BaseModelMixin(models.Model):
    """全局继承基类
    """
    add_date = models.DateTimeField("添加时间", auto_now_add=True)
    pub_date = models.DateTimeField("修改时间", auto_now=True)
    is_del = models.BooleanField(default=False)
    
    # TODO

    class Meta:
        abstract = True


class CarouselModelMixin(BaseModelMixin):
    """ 轮播图基类 """
    img = models.ImageField("轮播图", upload_to="happyshop/carousel/", max_length=200)
    img_url = models.CharField("外链图片", max_length=50, default="", blank=True)
    target_url = models.URLField("跳转链接", max_length=200, blank=True, default="")
    sort = models.PositiveIntegerField("排序", default=0)

    class Meta:
        ordering = ['-sort']
        abstract = True


class HappyShopBanner(CarouselModelMixin):
    """ Banner
    """

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.img.url