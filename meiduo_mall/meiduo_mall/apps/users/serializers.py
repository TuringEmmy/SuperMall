import re

from django.conf import settings
from django_redis import get_redis_connection
from rest_framework import serializers

# 发送邮件使用
from django.core.mail import send_mail

from goods.models import SKU
from users.constants import USER_BROWSING_HISTORY_COUNTS_LIMIT
from users.models import User, Address


# =================================用户浏览记录的序列化器============================
class BrowseHistorySerializer(serializers.Serializer):
    """浏览历史序列化器类"""
    sku_id = serializers.IntegerField(label='商品skud的编号', min_value=1)

    def validate_sku_id(self, value):
        """sku_id商品是否存在"""
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError("商品不存在")

        return value

    # 重写create方法
    def create(self, validated_data):
        """在redis中保存登陆用户的浏览记录"""
        # 因为商品浏览记录存在redis当中，所以在setting当中在天价一个caches的设置

        user = self.context['request'].user

        # 获取redis的链接
        redis_conn = get_redis_connection('histories')

        history_key = 'history_%s' % user.id

        # 添加浏览记录
        sku_id = validated_data['sku_id']
        # 去重：如果用户已经浏览过该商品,讲该商品的sku_id从list列表中移除
        # lrem(key,count,value)  :从redis列表中移除元素，有则移除，无则忽略

        # +++++++++++++++++++++++=创建管道对象++++++++++++++++++++++++++
        pl = redis_conn.pipeline()
        # redis_conn.lrem(history_key,0,sku_id)
        pl.lrem(history_key, 0, sku_id)

        # 左侧加入：保持浏览顺序
        # lpush(key,count,value)：从redis列表左侧加入元素
        # redis_conn.lpush(history_key,sku_id)
        pl.lpush(history_key, sku_id)

        # 截取：只保留最新的几个浏览记录
        # ltrim(key,start,stop)
        # redis_conn.ltrim(history_key,0,USER_BROWSING_HISTORY_COUNTS_LIMIT-1)
        pl.ltrim(history_key, 0, USER_BROWSING_HISTORY_COUNTS_LIMIT - 1)

        # 一次性执行
        pl.execute()

        return validated_data
        """
        注意：create平时返回的是对象，在这里可以直接返回validated_data
        上面三次的redis_conn可以创建管道，
        """


# ==============================邮箱验证的序列化器============================
class EmailSerializer(serializers.ModelSerializer):
    """邮箱学历恶化器类"""

    class Meta:
        model = User
        fields = ('id', 'email')

        # 对于emaill的，django里面自由有，所以不用砸门自己进行编写校验的逻辑

    def update(self, instance, validated_data):
        """设置登录用户的邮箱病给用户邮箱发送验证邮件"""
        # 设置登陆用户的=邮箱
        email = validated_data['email']
        instance.email = email
        instance.save()

        # TODO: 给用户邮箱发送验证邮件

        # 给用户邮箱发送邮箱验证重需要包含一个验证的链接地址
        # http://www.meiduo.site:8080/success_verify_email.html?user_id=<user_id>
        # 这样的url容易让别人恶意的请求

        # 链接地址：http://www.meiduo.site:8080/success_verify_email.html?token=<token>
        # token当中包含用户的信息
        # 因为每个用户都修妖这个操作，所以放在user的模型类的当中比较好
        verify_url = instance.generate_verify_url()

        # 发送emial邮箱发送验证邮件
        # subject = "美多商城邮箱验证"
        #
        # html_message = '<p>尊敬的用户您好！</p>' \
        #            '<p>感谢您使用美多商城。</p>' \
        #            '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
        #            '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
        # send_mail(subject, "", settings.EMAIL_FROM, [email], html_message=html_message)

        # =========================启用多进程========================
        from celery_tasks.email.tasks import send_verify_email
        send_verify_email(email, verify_url)
        # =========================启用多进程========================

        # 返回instance
        return instance


"""
send_mail(subject, message, from_email, recipient_list,html_message=None)

subject 邮件标题
message 普通邮件正文， 普通字符串
from_email 发件人
recipient_list 收件人列表
html_message 多媒体邮件正文，可以是html字符串



注意双面又是一个需要立即额作出应答的代码,抽取出来使用多进程
"""


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


# ===================================地址序列化器===============================
class UserAddressSerializer(serializers.ModelSerializer):
    """
    用户地址序列化器
    """
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)

    class Meta:
        model = Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')

    def validate_mobile(self, value):
        """
        验证手机号
        """
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def create(self, validated_data):
        """
        保存
        """
        # 在视图里面拿user是这样的,request.user,而在serializer里面通过context['resuest']
        # ['view'],['format']
        # 这些是在GenericAPIView里面子自带的属性获取方法
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AddressTitleSerializer(serializers.ModelSerializer):
    """
    地址标题
    """

    class Meta:
        model = Address
        fields = ('title',)
