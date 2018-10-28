from django.test import TestCase

# Create your tests here.
from itsdangerous import BadData


def urlencode_stu():
    # 将字典转化为字符串
    from urllib.parse import urlencode

    req_data = {
        'name': 'turing',
        'age': 23,
        'address': 'shanxi'
    }

    res = urlencode(req_data)

    return res


# 查询字符串转化为python的字典
def parse_qs_study():
    from urllib.parse import parse_qs
    req_str = "address=shanxi&name=turing&age=23"

    res = parse_qs(req_str)
    # 注意：字典的键值是list
    return res


# 发起http网络请求
def urlopen_stu():
    from urllib.request import urlopen

    req_url = 'http://api.meiduo.site:8000/mobiles/15313088696/count/'

    # 调用urlopen发起的http请求，返回值是一个相应对对象
    res = urlopen(req_url)

    # 获取相应数据
    res_data = res.read()
    return res_data


from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer


# itsdangerous 数据的加密解密
def data_jiami():
    # serializer = TJWSSerializer(secret_key='迷药',expires_in="有效时间")
    serializer = TJWSSerializer(secret_key='turing', expires_in=3600)

    req_data = {
        'openid': "SDHFJAKHDSJKLFHKLSDHAKJFHJKDSAHASDFHKJ"
    }

    res_data = serializer.dumps(req_data)

    res_str = res_data.decode()
    return res_str


# 数据解密
def data_jiemi():
    # 解密的内容
    req_str = 'eyJhbGciOiJIUzUxMiIsImV4cCI6MTU0MDcyMDYxMSwiaWF0IjoxNTQwNzE3MDExfQ.eyJvcGVuaWQiOiJTREhGSkFLSERTSktMRkhLTFNESEFLSkZISktEU0FIQVNERkhLSiJ9.UkEgNEvqKF2z2-80PY5GFG3l-fDNreDfGO-RdpjMI7sWSX8jac2KE0rPC8gqHLure9gBTrm7KFnou7gc0Ocs7Q'

    serializer = TJWSSerializer(secret_key='turng')

    # 注意解密可呢过会出现错误
    req_data = ''
    try:
        req_data = serializer.loads(req_str)
    except BadData as e:
        print("解密失败")
    return req_data


if __name__ == '__main__':
    print(data_jiami())

    print(data_jiemi())

if __name__ == '__main__':
    """urllib的使用"""
    # print(urlencode_stu())
    #
    # print(parse_qs_study())
    #
    # print(urlopen_stu())


    # age=23&name=turing&address=shanxi
    # {'age': ['23'], 'name': ['turing'], 'address': ['shanxi']}
    # b'{"mobile":"15313088696","count":1}'
