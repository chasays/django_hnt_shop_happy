from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from .models import BaseModelMixin

User = get_user_model()


class HappyShopRate(BaseModelMixin):
    """通用打分模型
    可关联任何模型进行打分
    """
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    rate = models.PositiveIntegerField("得分")
    comment = models.CharField("评价", max_length=300)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-add_date']
    
    def __str__(self):
        return self.comment