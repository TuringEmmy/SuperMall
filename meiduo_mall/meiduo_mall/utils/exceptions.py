# author    python
# time      18-10-25 下午3:18
# project   SuperMall

# 获取在配置文件的中定义的logger, 用来记录日志
import logging

from django.db import DatabaseError
from redis import RedisError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as eh

logger = logging.getLogger('django')



def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常
    :param context:抛出异常的上下文
    :return: Response相应对象
    """

    # 调用drf框架原声的异常处理方法
    response = eh(exc, context)

    if response is None:
        view = context['view']

        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s] %s ' % (view, exc))
            response = Response({
                'message':"服务器内部错误"
            },
            status=status.HTTP_507_INSUFFICIENT_STORAGE)
        return response