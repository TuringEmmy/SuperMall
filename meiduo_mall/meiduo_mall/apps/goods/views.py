from django.shortcuts import render

# Create your views here.
from rest_framework.filters import OrderingFilter

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU

# class SKUListView(APIView):
from goods.serializers import SKUSerializer, SKUIndexSerializer

# ---------------------------搜索引擎类------------------------------


from drf_haystack.viewsets import HaystackViewSet


# 编写搜索视图代码
# /sku/search/?text=<搜索关键词>
class SKUSearchViewSet(HaystackViewSet):
    """搜索引擎视图集"""
    """指定索引对应的模型类"""
    index_models = [SKU]

    # 搜索时候的需要一个序列化器类，而这个需要自己编写
    # 序列化是采用的序列化器类自行解决

    # -----------------------------
    # 搜索结果中包含两个属性：
    # text:索引字段的内容
    # object:搜索模型对象（此处是商品SKU对象）
    serializer_class = SKUIndexSerializer

# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------sku商品视图类---------------------------
# ===================商品列表视图==============================
# GET /categories/(?P<category_id>\d+)/skus/

# class SKUListView(GenericAPIView):
class SKUListView(ListAPIView):
    """"""

    serializer_class = SKUSerializer

    def get_queryset(self):
        """返回当前视图的查询集"""
        category_id = self.kwargs['category_id']
        return SKU.objects.filter(category_id=category_id, is_launched=True)

    # 设置排序的操作
    filter_backends = [OrderingFilter]

    # 指定排序的字段
    ordering_fields = ('create_time', 'price', 'sales')

    # def get(self,request, category_id):
    #     """
    #     获取第三季分类ID商品SKU商品的数据
    #     :param request:
    #     :param category_id:
    #     :return:
    #     1. 根据category_id商品的数据
    #     2. 讲商品的数据序列化返回
    #     """
    #     # 1. 根据category_id商品的数据
    #     # skus = SKU.objects.filter(category_id=category_id, is_launched = True)
    #
    #     skus = self.get_queryset()
    #
    #
    #     # 2. 讲商品的数据序列化返回
    #     serializer =self.get_serializer(skus,many=True)
    #
    #     return Response(serializer.data)


"""
# 获取查询的skus，紧急需要序列化，所以继承GenerticAPIView
通过查询的数据，为了方便将查询的对象昂返回，进一步使用get_serializer把数据进行反序列化，并返回
反思：这个是所有的数据进行查询，那么，是否有更高及的做法呐，直接查询ListAPIView

但是：慎重，这里没有category_id这个参数，所以拼凑数据的税后，query_set使无法查询到的

对于类视图有一个属性，self.kwargs

所以重写get_queryset函数，返回query_set函数
然后呐，数据拼凑好了，那么直接继承高级版本
ListAPIView

然后ok
"""
