from django.shortcuts import render
from django_redis import get_redis_connection

from rest_framework import status
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView

# 权限管理的
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from goods.models import SKU
from goods.serializers import SKUSerializer
from users import serializers
from users import constants
from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer, EmailSerializer, BrowseHistorySerializer


# ======================================历史访问记录====================
# POST /browse_histories/
# class BrowseHistoryView(APIView):
# class BrowseHistoryView(GenericAPIView):
class BrowseHistoryView(CreateAPIView):
    # 添加权限
    permission_classes = [IsAuthenticated]
    serializer_class = BrowseHistorySerializer

    def get(self, request):
        """
        登陆用户的浏览记录
        :param request:
        :return:
        1. 从redis中获取登录用户浏览的商品的id
        2. 根据商品的sku_id获取对应的商品的信息
        3. 将商品的数据序列化并返回
        """

        # 获取用户登陆
        user = request.user
        # 1. 从redis中获取登录用户浏览的商品的id
        redis_conn = get_redis_connection('histories')

        history_key = 'history_%s' % user.id

        # lrange(key,start,stop):获取redis列表的指定区间内容元素
        # [b'<sku_id>,b'<sku_id>]   -1取所有
        sku_ids = redis_conn.lrange(history_key, 0, -1)
        # 2. 根据商品的sku_id获取对应的商品的信息
        skus = []

        for sku_id in sku_ids:
            # 虽然这里是bytes类型的，但是不需要进行个是的转换，因为他会自动进行转换
            sku = SKU.objects.get(id=sku_id)
            skus.append(sku)
        # 3. 将商品的数据序列化并返回
        serializer = SKUSerializer(skus,many=True)

        return Response(serializer.data)




    # def post(self, request):
    #     """
    #     历史浏览记录的添加
    #     :param request:
    #     :return:
    #     1. 获取商品的sku_id病进行校验（sku_id必传,sku_id商品是否存在）
    #     2. redis中保存登陆用户的浏览记录
    #     3. 返回应答，浏览记录保存用户
    #     """
    #     # 1. 获取商品的sku_id病进行校验（sku_id必传,sku_id商品是否存在）
    #     serializers = self.get_serializer(data=request.data)
    #
    #     # 2. redis中保存登陆用户的浏览记录(create)
    #     serializers.save()
    #     # 3. 返回应答，浏览记录保存用户
    #
    #     # 返回的serializer.data就是create返回的validated_data
    #     return Response(serializers.data,status=status.HTTP_201_CREATED)


"""
一上来，视图首先继承APIView,为了方便，编写一个serializer，然后直接换成GenericAPIView
,
再进行反思，这个创建一条记录的代码，可以使用更高高级的做法

CreateAPIView视图来完成这个

还有一点需要注意的是创建后的，拼凑数据不需要进行数queryset的拼凑，因为他毫无价值，这一点需要格外注意
"""


# Create your views here.





# =================================邮箱验证的处理==============================
# email/verification/
class EmailVerifyView(APIView):
    """
       邮箱验证
       """

    def put(self, request):
        # 获取token
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '缺少token'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证token
        user = User.check_verify_email_token(token)
        if user is None:
            return Response({'message': '链接信息无效'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.email_active = True
            user.save()
            return Response({'message': 'OK'})


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


# ===============================================用户地址视图===========================
class AddressViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    用户地址新增与修改
    """
    serializer_class = serializers.UserAddressSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

    # GET /addresses/
    def list(self, request, *args, **kwargs):
        """
        用户地址列表数据
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'addresses': serializer.data,
        })

    # POST /addresses/
    def create(self, request, *args, **kwargs):
        """
        保存用户地址数据
        """
        # 检查用户地址数据数目不能超过上限
        count = request.user.addresses.filter(is_deleted=False).count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return Response({'message': '保存地址数据已达到上限'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    # delete /addresses/<pk>/
    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # put /addresses/pk/status/
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    # put /addresses/pk/title/
    # 需要请求体参数 title
    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        """
        修改标题
        """
        address = self.get_object()
        serializer = serializers.AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
