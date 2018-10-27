import random

from django.shortcuts import render

# Create your views here.


# url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_mall.libs.yuntongxun.sms import CCP
from veritifications import constants

# 获取日志器

import logging

logger = logging.getLogger('django')


# url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
class SMSCodeView(APIView):
    def get(self, request, mobile):
        """
        短信验证码
        1. 随机生成6位数字作为短信验证码的内容g
        2. 在redis中存储短信验证码的内容,以mobile位key,以短信验证码位value
        3. 使用云通讯给mobile发送带短信验证码
        4 .返回应答,发送成功

        """
        # 判断短信验证码,判断是否在60s内
        redis_conn = get_redis_connection("verify_codes")

        send_flag = redis_conn.get('send_flag_%s' % mobile)

        if send_flag:
            return Response({'message': '发送短信你国语频繁'}, status=status.HTTP_400_BAD_REQUEST)

        # ----------------------------生成验证码----------------------------------------
        sms_code = "%06d" % random.randint(0, 999999)

        logger.info("短信验证码位:%s" % sms_code)

        # -----------------------保存短信验证码与发送记录-----------------------------------
        # 创建redis管道中添加命令[建立一次链接,可以多次批量输入命令]
        pl = redis_conn.pipeline()

        # redis_conn.setex('<key>', '<expires>', '<value>')
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 批量执行管道中所有的命令
        pl.execute()

        # ---------------------------使用云通讯给mobile发送短信验证码------------------------------
        expires = constants.SMS_CODE_REDIS_EXPIRES // 60

        # try:
        #     res = CCP().send_template_sms(mobile, [sms_code, expires], constants.SMS_CODE_TEMP_ID)
        # except Exception as e:
        #     logging.error(e)
        #     return Response({'message': '发送短信异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        #
        # if res != 0:
        #     return Response({'message': "发送短信失败"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        #
        # # -------------------------------返回应答,发送成功----------------------------------------
        # # form celery_ta

        # # 发送短信验证码
        # from celery_tasks.sms.tasks import send_sms_code
        # send_sms_code.delay(mobile, sms_code, expires)

        return Response({"message": "OK"})
