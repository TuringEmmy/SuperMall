# author    python
# time      18-10-25 下午10:02
# project   SuperMall
import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.settings import api_settings

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """创建用户序列化器"""

    token = serializers.CharField(label='登陆状态token',read_only=True)

    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)

    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow','token')

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
        """验证手机号码"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("手机号码格式错误")

        # 手机号码是否重复
        count = User.objects.filter(mobile=value).count()
        if count > 0:
            raise serializers.ValidationError("手机号码已经存在")

        return value

    def validate_allow(self, value):
        """检验用户是否同意协议"""

        if value != 'true':
            raise serializers.ValidationError("晴统一要协议")

        return value

    # =======================判断两次密码是否一致==================================
    def validate(self, data):

        # 判断两次密码
        if data['password'] != data['password2']:
            raise serializers.ValidationError("两次密码不一样")

        # 判断短信验证码
        redis_conn = get_redis_connection('verify_codes')

        mobile = data['mobile']

        real_sms_code = redis_conn.get('sms_%s' % mobile)

        if real_sms_code is None:
            raise serializers.ValidationError("无效的短信验证码")

        return data

    # =======================创建用户===============================
    def create(self, validated_data):
        """创建用户"""

        # 移除数据库模型类中不存在的属性，因为这些信息只是在注册的时候使验证使用，之后没有用，存入数据库也不需要
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        user = super().create(validated_data)

        # 调用django的认证加密密码
        user.set_password(validated_data['password'])

        user.save()


        # ======================补充生成记录状态的token===========
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token


        return user
