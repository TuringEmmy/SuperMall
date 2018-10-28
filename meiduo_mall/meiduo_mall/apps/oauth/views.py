from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class QQAuthURLView(APIView):
    """返回qq认证接口的url"""
    """
    接口文档说明
    1. url /oauth/qq/statues/
    2. 请求方式  GET
    3. 请求参数
    4. 返回相应  json(qq认证接口的认证)
    """
    def get(self, request):

        pass
