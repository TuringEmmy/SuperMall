# author    python
# time      18-10-28 下午3:30
# project   SuperMall
from django.db import models


class BaseModel(models.Model):
    create_time = models.DateField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateField(auto_now=True,verbose_name='更新时间')

    class Meta:
        # 说明这是一个抽象类型类，在进行模型的迁移的当中不会生成 表
        abstarct = True
    pass