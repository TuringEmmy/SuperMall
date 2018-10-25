from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users import serializers
from users.models import User


# ===========================判断用户名是否村存在====================================
# GET /usernames/(?P<username>\w{5,20})/count/
class UsernameCountView(APIView):
    """用户名数量"""

    def get(self, request, username):
        """获取指定用户名数量"""

        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)


# ============================判断手机号码是否存在===================================
# GET /mobiles/(?P<mobile>1[3-9]\d{9})/count
class MobileCountView(APIView):
    """手机号数量"""

    def get(self, request, mobile):
        """获取手机号数量"""
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count,
        }

        return Response(data)


# =================================用户注册=========================================
# /users/


class UserView(CreateAPIView):
    """
    用户注册
    username,password,password3,sms_code,mobile,allow
    """
    serializer_class = serializers.CreateUserSerializer
