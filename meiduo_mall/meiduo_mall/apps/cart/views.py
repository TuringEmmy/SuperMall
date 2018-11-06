import base64
import pickle
from django.shortcuts import render

# Create your views here.

# POST /cart/
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.constants import CART_COOKIE_EXPIRES
from cart.serializers import CartSerializer, CartSKUSerializer, CartDelSerializer

# POST /cart/
from goods.models import SKU


class CartView(APIView):
    def perform_authentication(self, request):
        """让当前视图跳过DRF框架的认证过程"""
        pass

    # 商品的删除
    def delete(self, request):
        """
        购物车记录删除:
        1. 获取sku_id并进行校验(sku_id对应商品是否存在)
        2. 删除用户的购物车记录
            2.1 如果用户已登录，删除redis中对应的购物车记录
            2.2 如果用户未登录，删除cookie中对应的购物车记录
        3. 返回应答，购物车记录删除成功
        """
        # 1. 获取sku_id并进行校验(sku_id对应商品是否存在)
        serializer = CartDelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 获取校验之后的数据
        sku_id = serializer.validated_data['sku_id']

        try:
            user = request.user
        except Exception:
            user = None

        # 2. 删除用户的购物车记录
        if user is not None and user.is_authenticated:
            # 2.1 如果用户已登录，删除redis中对应的购物车记录
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()

            # 在redis hash元素中删除用户购物车记录中商品的id和对应数量count
            cart_key = 'cart_%s' % user.id
            # hdel(key, *fields): 删除hash中指定属性和值，如果属性不存在，直接忽略
            pl.hdel(cart_key, sku_id)

            # 在redis set元素中移除用户购物车记录中商品的勾选状态
            cart_selected_key = 'cart_selected_%s' % user.id

            # srem(key, *members): 从set集合中移除元素，有则移除，无则忽略
            pl.srem(cart_selected_key, sku_id)

            pl.execute()

            # 返回应答
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT)
            # 2.2 如果用户未登录，删除cookie中对应的购物车记录
            cookie_cart = request.COOKIES.get('cart')  # None

            if cookie_cart is None:
                # 购物车无数据
                return response

            # 解析cookie中的购物车数据
            # {
            #     '<sku_id>': {
            #         'count': '<count>',
            #         'selected': '<selected>'
            #     },
            #     ...
            # }
            cart_dict = pickle.loads(base64.b64decode(cookie_cart))  # {}

            if not cart_dict:
                # 字典为空，购物车无数据
                return response

            # 删除购物车对应记录
            if sku_id in cart_dict:
                del cart_dict[sku_id]
                cart_data = base64.b64encode(pickle.dumps(cart_dict)).decode()
                response.set_cookie('cart', cart_data, max_age=CART_COOKIE_EXPIRES)

            # 3. 返回应答，购物车记录删除成功
            return response

    # 商品修改
    def put(self, request):
        """
        购物车记录修改:
        1. 获取参数并进行校验(sku_id商品是否存在，商品库存是否足够)
        2. 修改用户的购物车记录
            2.1 如果用户已登录，修改redis中的购物车记录
            2.2 如果用户未登录，修改cookie中的购物车记录
        3. 返回应答，购物车记录修改成功
        """
        # 1. 获取参数并进行校验(sku_id商品是否存在，商品库存是否足够)
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 获取校验之后的数据
        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']
        selected = serializer.validated_data['selected']

        try:
            user = request.user
        except Exception:
            user = None

        # 2. 修改用户的购物车记录
        if user is not None and user.is_authenticated:
            # 2.1 如果用户已登录，修改redis中的购物车记录
            redis_conn = get_redis_connection('cart')

            # 在redis hash元素修改购物车中对应商品的数量count
            cart_key = 'cart_%s' % user.id
            # hset(key, field, value): 将hash中指定属性field值设置为value
            redis_conn.hset(cart_key, sku_id, count)

            # 在redis set元素修改购物车中商品的勾选状态
            cart_selected_key = 'cart_selected_%s' % user.id
            if selected:
                # 勾选
                # sadd(key, *members): 向set集合中添加元素
                redis_conn.sadd(cart_selected_key, sku_id)
            else:
                # 取消勾选
                # srem(key, *members): 从set集合中移除元素，有则移除，无则忽略
                redis_conn.srem(cart_selected_key, sku_id)

            return Response(serializer.data)
        else:
            response = Response(serializer.data)
            # 2.2 如果用户未登录，修改cookie中的购物车记录
            cookie_cart = request.COOKIES.get('cart')  # None

            if cookie_cart is None:
                # 购物车无数据
                return response

            # 解析cookie中的购物车数据
            # {
            #     '<sku_id>': {
            #         'count': '<count>',
            #         'selected': '<selected>'
            #     },
            #     ...
            # }
            cart_dict = pickle.loads(base64.b64decode(cookie_cart))  # {}

            if not cart_dict:
                # 字典为空，购物车无数据
                return response

            if sku_id in cart_dict:
                cart_dict[sku_id] = {
                    'count': count,
                    'selected': selected
                }

            # 3. 返回应答，购物车记录修改成功
            # 处理cookie购物车数据
            cart_data = base64.b64encode(pickle.dumps(cart_dict)).decode()
            response.set_cookie('cart', cart_data, max_age=CART_COOKIE_EXPIRES)
            return response


    def get(self, request):
        """
        购物城记录获取
        1. 获取用户的购物记录
            1.1 如果用户一登录，从redis中获取购物车记录
            1.2 如果用户未登录，从cookies中获取用户的购物信息
        2. 根据用户购物车中商品的kus_id获取对应的商品信息
        3. 将购物车商品的数据序列化并返回
        :param request:
        :return:
        """
        try:
            user = request.user
        except Exception:
            user = None

        # 1. 获取用户的购物记录
        if user is not None and user.is_authenticated:
            #     1.1 如果用户一登录，从redis中获取购物车记录
            redis_conn = get_redis_connection('cart')
            # 从redis hash元素中获取用户购物车中添加的商品id和对应数量的count
            cart_key = 'cart_%s' % user.id

            cart_redis = redis_conn.hgetall(cart_key)
            # {
            #     b'sku_id':count
            # }

            # 从redis set元素中获取用户购物车当中被勾选的商品id
            cart_selected_key = 'cart_selected_%s' % user.id
            # (b'sku_id',b'sku_id')
            cart_redis_selected = redis_conn.smembers(cart_selected_key)

            # ===+++++++++++++组织数据+++++++++===
            cart_dict = {}
            for sku_id, count in cart_redis.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_redis_selected
                }


        else:

            #     1.2 如果用户未登录，从cookies中获取用户的购物信息
            cookie_cart = request.COOKIES.get('cart')  # None

            if cookie_cart:
                """解析cookies中的购物车信息"""
                # {
                #     'sku_id':{
                #         'count':count,
                #         'selected':seleceted,
                #     }
                # }
                cart_dict = pickle.loads(base64.b64decode(cookie_cart))
            else:
                cart_dict = {}
        # 2. 根据用户购物车中商品的kus_id获取对应的商品信息
        sku_ids = cart_dict.keys()

        skus = SKU.objects.filter(id__in=sku_ids)

        for sku in skus:
            # 给sku商品增加对象属性count和selected
            # 分别保存该商品在用户购物车中添加的商品的数量勾选状态
            sku.count =cart_dict[sku.id]['count']
            sku.selected = cart_dict[sku.id]['selected']


        # 3. 将购物车商品的数据序列化并返回
        serializer = CartSKUSerializer(skus,many=True)
        # 返回序列化数据
        return Response(serializer.data)

    # 存储购物车
    def post(self, request):
        """
        购物车和记录添加
        1. 接受参数病进行校验(sku_id商品是否存在，商品库存是否足够)
        2. 保存用户的购物车记录
            2.1 如果用户已登陆，在redis中保存用户的购物车记录
            2.2 如果用户未登录，在cookies中保存用户的购物车记录
        3. 返回应答，购物车记录保存成功
        :param request:
        :return:
        """
        # 1. 接受参数病进行校验(sku_id商品是否存在，商品库存是否足够)
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 获取校验之后的数据
        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']
        selected = serializer.validated_data['selected']

        # 获取user
        try:
            # request.user 会触发DRF框架的认证过程，此处如果jwt token 认证失败，说明用户未登录
            # 不需要给客户返回存储，所以自己可以进行try...except处理
            user = request.user
        except Exception:
            user = None

        # 2. 保存用户的购物车记录
        if user is not None and user.is_authenticated:
            # 2.1 如果用户已登陆，在redis中保存用户的购物车记录
            # 获取redis链接
            redis_conn = get_redis_connection('cart')
            # 在redis hash元素中存用户添加到购物车商品的id和对应的count

            """
            redis_conn是使用管道,
            """

            pl = redis_conn.pipeline()
            cart_key = 'cart_%s' % user.id

            # 如果用户的购物车已经添加该商品，数量count需要进行累加
            # hincrby(key,field,count):给hash中指定属性field的值累加count，如果属性和值不存在，会新建属性
            # redis_conn.hincrby(cart_key, sku_id, count)
            pl.hincrby(cart_key, sku_id, count)

            # 在redis set元素中各存用户添加的购物车的中被勾选的商品的id

            cart_selected_key = 'cart_selected_%s' % user.id

            if selected:
                # 记录被勾选
                # sadd(key,*members):向set集合中添加元素，集合中元素是唯一的
                # redis_conn.sadd(cart_selected_key, sku_id)
                pl.sadd(cart_selected_key, sku_id)

            pl.execute()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 2.2 如果用户未登录，在cookies中保存用户的购物车记录

            # 获取客户端传递的数据
            cookie_cart = request.COOKIES.get('cart')

            # 这个恶有可能回事空值
            if cookie_cart:
                # 解析cookies中购物车的数据
                # {
                #     'sku_id':{
                #         'count':count,
                #         'selected':selected,
                #     }
                # }
                cart_dict = pickle.loads(base64.b64decode(cookie_cart))

            else:
                cart_dict = {}

            # 保存用户添加的购物车数据
            if sku_id in cart_dict:
                # 如果存在数据，则进行累加操作
                count += cart_dict[sku_id]['count']

            cart_dict[sku_id] = {
                'count': count,
                'selected': selected,
            }

            # 返回相应
            response = Response(serializer.data, status=status.HTTP_201_CREATED)

            # 将字典转换为str的字符串并存储到客户端的浏览器当中ing
            # cart_data = base64.b64decode(pickle.dumps(cart_dict)).decode()   # str
            cart_data = base64.b64encode(pickle.dumps(cart_dict)).decode()  # str

            response.set_cookie('cart', cart_data, max_age=CART_COOKIE_EXPIRES)

            # 返回响应
            return response
            # 3. 返回应答，购物车记录保存成功
