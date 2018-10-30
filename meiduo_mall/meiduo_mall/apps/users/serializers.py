import re

from django_redis import get_redis_connection
from rest_framework import serializers

from users.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    """这个只是用作序列化器"""

    class Meta:
        model = User

        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class UserSerializer(serializers.ModelSerializer):
    """用户注册序列化器类"""
    password2 = serializers.CharField(label='重复密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='jwt token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'password2', 'sms_code', 'allow', 'token')

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):
        """手机号格式，手机号是否已注册"""
        # 手机号格式
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')

        # 手机号是否已注册
        res = User.objects.filter(mobile=value).count()

        if res > 0:
            raise serializers.ValidationError('手机号已注册')

        return value

    def validate_allow(self, value):
        """是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请同意协议')

        return value

    def validate(self, attrs):
        """两次密码是否一致，短信验证码是否正确"""
        # 两次密码是否一致
        password = attrs['password']
        password2 = attrs['password2']

        if password != password2:
            raise serializers.ValidationError('两次密码不一致')

        # 短信验证码是否正确
        mobile = attrs['mobile']

        # 从redis中获取真实的短信验证码内容
        redis_conn = get_redis_connection('verify_codes')
        # bytes
        real_sms_code = redis_conn.get('sms_%s' % mobile)  # None

        if real_sms_code is None:
            raise serializers.ValidationError('短信验证码已过期')

        # 对比短信验证码
        sms_code = attrs['sms_code']  # str

        if sms_code != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    def create(self, validated_data):
        """创建新用户并保存注册用户的信息"""
        # 清除无用的数据
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        # 创建并保存新用户
        user = User.objects.create_user(**validated_data)

        # 由服务器生成jwt token数据，保存用户的身份信息
        from rest_framework_jwt.settings import api_settings

        # 组织payload的数据
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成jwt token
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 生成payload数据
        payload = jwt_payload_handler(user)
        # 生成jwt token数据
        token = jwt_encode_handler(payload)

        # 给user对象增加属性token，保存jwt token数据
        user.token = token

        # 返回user
        return user
