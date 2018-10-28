from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from oauth.exceptions import QQAPIError
from oauth.models import OAuthQQUser
from oauth.serializers import QQAuthUserSerializer
from oauth.utils import OAuthQQ


# GET /oauth/qq/authorization/?next=<登陆跳转地址>
class QQAuthURLView(APIView):
    """返回qq认证接口的url"""
    """
    接口文档说明
    1. url /oauth/qq/statues/
    2. 请求方式  GET
    3. 请求参数
    4. 返回相应  json(qq认证接口的认证)

    获取QQ登陆网址
    1. 获取next
    2. 组织QQ登陆的网址参数
    3. 返回QQ登陆的网站
    """

    def get(self, request):
        # 1.获取next
        next = request.query_params.get('next', '/')

        # 2.组织QQ登陆的网址参数
        oauth = OAuthQQ(state=next)

        login_url = oauth.get_login_url()

        # 3.返回QQ登陆的网站
        return Response({"login_url": login_url})

    def post(self, request):
        """
        保存绑定QQ登陆用户信息
        1.获取参数并进行校验(参数完整，手机号格式，大圩您验证码是否正确，access_token是否有效)
        2.保存绑定QQ登陆用户的数据
        3.返回应答
        :param request:
        :return:
        """

        # 1.获取参数并进行校验(参数完整，手机号格式，大圩您验证码是否正确，access_token是否有效)

        # 2.保存绑定QQ登陆用户的数据

        # 3.返回应答


# GET /oauth/qq/user/?code=<code>
# class QQAuthUserView(APIView):
class QQAuthUserView(GenericAPIView):
    serializer_class = QQAuthUserSerializer

    def post(self, request):
        """
        保存绑定QQ登陆用户信息
        1.获取参数并进行校验
        2.保存绑定QQ登陆用户的数据
        3.返回应答
        :param request:
        :return:
        """
        # 1.获取参数并进行校验
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2.保存绑定QQ登陆用户的数据(create)
        serializer.save()
        # 3.返回应答

    def get(self, request):
        """
        获取QQ登陆用户的openid
        1.获取code并校验
        2.获取QQ登陆用户的ID
            2.1根据code请求QQ服务器获取access_token
            2.2根据access_token服务器获取toekn并返回
        3.根据openid进行处理
            3.1如果openid绑定过本网站,直接签发jwt token并返回
            3.2如果openid为绑定过本网扎用户,对openid进行加密病返回
        :param request:
        :return:
        """
        # 获取code并校验
        code = request.query_params.get('code')  # 必传

        if code is None:
            return Response({'message': "缺少code参数"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取Qq灯笼裤用户的openid
        oauth = OAuthQQ()

        try:
            # 根据code请求QQ服务器获取access_token
            access_token = oauth.get_access_token(code=code)
            # 根据access_token获取openid
            openid = oauth.get_openid(access_token=access_token)
        except QQAPIError:
            # 服务不可用
            return Response({"message": "QQ登陆遗异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # ======================根据openid判断是否绑定过==============================
        try:
            qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 不存在,则需要进行绑定,并对openid进行加密

            # 类方法直接调用
            token = OAuthQQ.generate_save_user_token(openid)
            return Response({'access_token': token})

        else:
            # 说明绑定过本网站,直接欠发达jwt token并返回

            # 通过外键关联在QQ表中查询外交按id
            user = qq_user.user

            # 由服务器生成jwt token数据,直接签发jwt token
            from rest_framework_jwt.settings import api_settings

            # 组织payload数据
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            # 生成jwt token
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            # 生成payload数据
            pay_load = jwt_payload_handler(user)

            # 生成jwt token数据
            token = jwt_encode_handler(pay_load)

            # 返回数据
            res_data = {
                'user_id': user.id,
                'username': user.username,
                'token': token
            }

            return Response(res_data)
