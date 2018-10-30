from django.db import models


# Create your models here.
class Area(models.Model):
    """地区模型类"""

    name = models.CharField(max_length=20, verbose_name='名称')

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True)

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = verbose_name


"""
这是一个自关联的模型类
通过父级id查询子级的行政去区划
"""

