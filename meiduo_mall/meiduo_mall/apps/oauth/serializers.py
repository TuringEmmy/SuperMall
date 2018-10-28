# author    python
# time      18-10-28 下午7:48
# project   SuperMall
import base64
import os

from django_redis import get_redis_connection
from rest_framework import serializers

from oauth.models import OAuthQQUser
from oauth.utils import OAuthQQ
from users.models import User


class QQAuthUserSerializer(serializers.ModelSerializer):
    # 因为是用的user信息，所以继承ModleSerializer

    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    access_token = serializers.CharField(label='openid加密内容', write_only=True)
    token = serializers.CharField(label='JWT Token', read_only=True)

    # 不在让他自动生成，我要自定义《里面有正则》
    mobile = serializers.RegexField(label='手机',regex=r'1[3-9\d{9}$',write_only=True)

    class Meta:
        model = User

        fields = (
            "mobile", 'password', 'sms_code', 'access_token', 'id', 'username', 'token'
        )

        extra_kwargs = {
            'username': {
                'read_only': True
            },
            # 'mobile': {
            #     'write_only': True
            # },
            'password': {
                'write_only': True,
                'min_length':8,
                'max_length':20,
                'error_messages':{
                    'min_length':"仅允许8-20个字符的密码",
                    'max_length':"仅允许8-20个字符串的密码"
                }
            }
        }


        # 手机格式利用regrex重写

    def validate(self, attrs):
        """短信验证码是否正确,access_token是否有效"""

        # access_token是否有效
        access_token = attrs['access_token']
        openid = OAuthQQ.check_save_user_token(access_token)


        if openid is None:
            raise serializers.ValidationError("无效的access_token")

        # 短信验证码是否正确
        mobile = attrs['mobile']

        # 从redis中获取真实的短信验证码

        redis_conn = get_redis_connection('verify_codes')

        real_sms_code = redis_conn.get('sms_%s'%mobile)

        if real_sms_code is None:
            raise serializers.ValidationError("短信验证码已经过期")

        # 对比短信验证码
        sms_code = attrs['sms_code']

        if sms_code != real_sms_code.decode():
            raise serializers.ValidationError("短信验证码错误")

        # 如果mobile已经注册 ，需要校验对应的密码是对方正确
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoseNotExist:
            # 用户未注册
            pass
        else:
            # 用户已注册，校验密码
            password = attrs['password']
            if not user.check_password(password):
                raise serializers.ValidationError("用户密码错误")


        # 给attrs字典添加元素user,以便在保存绑定QQ登陆用户的数据直接使用
        attrs['user'] = user


        attrs['openid']

        return attrs

        # validated_data 是校验后的attrs哦，小雍要注意啊哦

    def create(self, validated_data):
        """保存绑定QQ登陆用户的数据"""
        # 如果mobile没有注册，先创建新用户
        user = validated_data['user']

        if user is None:
            # 随机生成用户名
            username = base64.b64decode(os.urandom(13))
            password = validated_data['password']
            mobile = validated_data['mobile']
            user = User.objects.create(username=username,password=password,mobile=mobile)
        # 保存绑定QQ用户的数据
        OAuthQQUser.objects.create(
            user = user,
            openid = validated_data['openid']
        )

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

        user.token = token

        # 返回user
        return user