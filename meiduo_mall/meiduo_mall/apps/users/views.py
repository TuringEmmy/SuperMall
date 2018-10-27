from django.shortcuts import render
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from users.models import User
from users.serializers import UserSerializer
# Create your views here.


# POST /users/
class UserView(GenericAPIView):
    # 指定当前视图所使用的序列化器类
    serializer_class = UserSerializer

    def post(self, request):
        """
        保存注册用户的信息:
        1. 接收参数并进行校验(参数完整性，两次密码是否一致，手机号格式，手机号是否已注册，短信验证码是否正确，是否同意协议)
        2. 创建新用户并保存注册用户的信息
        3. 返回应答，注册成功
        """
        # 1. 接收参数并进行校验(参数完整性，两次密码是否一致，手机号格式，手机号是否已注册，短信验证码是否正确，是否同意协议)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. 创建新用户并保存注册用户的信息 (create)
        serializer.save()

        # 3. 返回应答，注册成功
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    """
    手机号数量
    """
    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)


# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
class UsernameCountView(APIView):
    """
    用户名数量
    """
    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)
