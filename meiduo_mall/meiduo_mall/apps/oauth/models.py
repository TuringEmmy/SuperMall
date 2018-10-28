from django.db import models

# Create your models here.
from meiduo_mall.utils.models import BaseModel


class OAuthQQUser(BaseModel):
    """
    QQ登陆用户数据
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    # 这个到时候会tb_oauth_qq表有个users_id

    openid = models.CharField(max_length=54, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登陆用户数据'
        verbose_name_plural = verbose_name
