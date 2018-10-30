from django.shortcuts import render
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView,UpdateAPIView

# 权限管理的
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer, EmailSerializer


# Create your views here.


# ========================================邮箱====================================
# PUT /email/
# class EmailView(APIView):
# class EmailView(GenericAPIView):
class EmailView(UpdateAPIView):
    # 这个也是要登陆用户才能的访问的
    permission_classes = [IsAuthenticated]

    # 牵扯到了序列化器类，所所以使用GenericAPIView
    serializer_class = EmailSerializer

    def get_object(self):
        """返回当前登陆的user"""
        return self.request.user
    #
    # def put(self, request):
    #     """
    #     设置登录用户的邮箱
    #     :param request:
    #     :return:
    #     1. 获取登陆用户的邮箱
    #     2. 获取emaill病进行校验（email,）
    #     3.设置登录用户邮箱病给用户邮箱验证邮件
    #     4,。返回应答，邮箱设置成功
    #     """
    #     # 1. 获取登陆用户的邮箱
    #     # user = request.user
    #
    #     self.get_object()
    #
    #     # 2. 获取emaill病进行校验（email,）
    #     # 其实这里也可以使用序列化器来完成
    #     serializer = self.get_serializer(data=request.data)
    #     # 验证序列
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 3.设置登录用户邮箱病给用户邮箱验证邮件update
    #     serializer.save()
    #     # 调用save函数的时候，要重写upodate的方法哦
    #
    #
    #     # 4。 返回应答，邮箱设置成功
    #     return Response(serializer.data)


"""
这里开始的思路也是继承APIView的视图，update user set email='yong2163.com' where id = 1;
然后获取邮箱，惯性思维就算着急又获取邮箱，也搞个序列化器，然后升级为GenericAPIView
还有一点很重要，这里进行了从前段获取email， 进行的是序列化，股需要进行校验参数的完整性
最后进行put函数的目标，执行sql语句，将其保存到数据库当中
并返回相应，给前段作出相应


但是，但是，注意了，这里是进行put操作记性update的操作
有了更高及的UpdateAPIView基进行，但是这个里面需要查询集，不谢get_objects的方法

"""


# ==============================================用户详情页的=============================
# GET /user/
# class UserDetailView(GenericAPIView):
class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    # 导入序列化器
    serializer_class = UserDetailSerializer

    # 重写get_object方法
    def get_object(self):
        """返回当前的user"""

        # 这个没有request的参数，可以使用self.request获取
        return self.request.user
        #
        # # 个人用户登陆需要权限管理
        # def get(self, request):
        #     """
        #     获取用户个人信息
        #     1. 获取登陆用户的user
        #     2. 将user数据序列化并返回
        #
        #
        #     补充：request拥有user属性（添加案件权限后会有认证用户和匿名用户之分）
        #     self.request就是请求的request对象
        #     """
        #     # 1. 获取登陆用户的user
        #     # user = request.user
        #     # 替换为下面的方法
        #     user = self.get_object()
        #
        #     # 2. 将user数据序列化并返回
        #     serializer = self.get_serializer(user)
        #     return Response(serializer.data)


"""
其实获取个人信息就是select * from user where id = pk
使用到了get方法
明显不是list方法，
因为获取单个用户的所以 是retrieve，自然而然就是RetrieveAPIView了，View肯定是舍弃的，最次也是APIView,然后使用到了序列化器，
升级为GenericAPIView,他里面有一个get_object的方法，默认按照id记性查询，这里因为已经登陆，直接可以获取当前用户，
所以self.request.user可以直接获取到
而Retieve刚刚好，默认写了get的方法，
所以代码再一次升级，删掉get方法，直接继承了RetieveAPIView类
"""


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
