from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


        # 注意:一定会要在setting当中进行设置AUTH_USER_MODEL = 'users.User'
        #     AUTH_USER_MODEL
        #     参数的设置以点.来分隔，表示应用名.模型类名。
        #
        #     注意：Django建议我们对于AUTH_USER_MODEL参数的设置一定要在第一次数据库迁移之前就设置好，否则后续使用可能出现未知错误。
