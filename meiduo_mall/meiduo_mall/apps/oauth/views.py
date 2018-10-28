from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

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

