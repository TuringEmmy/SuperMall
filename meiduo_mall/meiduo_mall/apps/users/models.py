from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, verbose_name='手机号')

    # openid 字段：记录和本网站用户绑定的QQ登陆用户的openid
    # 注意：一个用户可以绑定多个QQ用户
    openid = models.CharField()

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
