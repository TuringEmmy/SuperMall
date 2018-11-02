from django.db import models

# Create your models here.
class PicTest(models.Model):
    """FDFS文件上传测试模型类"""
    image = models.ImageField(verbose_name='图片')

    class Meta:
        db_table = 'tb_pic'
        verbose_name = 'FDFS图片上传测试'
        verbose_name_plural = verbose_name
