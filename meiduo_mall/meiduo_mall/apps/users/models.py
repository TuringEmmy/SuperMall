from django.contrib.auth.models import AbstractUser
from django.db import models


# 导入setting的配置文件
from django.conf import settings


# 这里钥匙用token，所以到导包
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer
# Create your models here.
from users import constants


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, verbose_name='手机号')

    # 添加邮箱
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_verify_url(self):
        """生成用户对应的邮箱验证链接地址"""
        data = {
            'id':self.id,
            'email':self.email,
        }

        # 创建TimedJSONWebSignatureSerializer对象

        # 这里秘钥使用setting 看里面当中的
        serializer = TJWSSerializer(secret_key=settings.SECRET_KEY,expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)


        # 对数据进行加密
        token = serializer.dumps(data)  # bytes


        # 生成验证的链接
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token='+token

        return verify_url





