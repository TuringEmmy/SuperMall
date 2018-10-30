from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

# GET /areas/
from rest_framework.viewsets import ReadOnlyModelViewSet

from areas.models import Area

# class AreasView(APIView):
from areas.serializers import AreaSerializer, SubAreaSeializer

# =====================反思,下面两个视图函数都是在进行查询=================
# ===================可以使用视图集=================================


class AreasViewSet(ReadOnlyModelViewSet):
    """地区视图集"""
    # 注意:这里需要进行分类了
    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubAreaSeializer
    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()

# ==========================================================



# GET /areas/(?P<pk>\d+)/
# class SubAreasView(APIView):
# class SubAreasView(GenericAPIView):
class SubAreasView(RetrieveAPIView):
    serializer_class = SubAreaSeializer

    queryset = Area.objects.all()

    # def get(self, request, pk):
    #     """
    #     获取指定地区的信息
    #     1.根据pk获取指定地区的信息
    #     2.讲指定地区序列化器返回(需要将会地区下级地区进行嵌套的学历恶化)
    #     :param request:
    #     :return:
    #     """
    #     # 1.根据pk获取指定地区的信息
    #     try:
    #         # area = Area.objects.get(pk=pk)
    #         area = self.get_objects()
    #     except Area.DoesNotExist:
    #         raise Http404
    #
    #     # 数据库库获取的=数据了,马上二话不收,反序列化,拆包,我拆包
    #
    #
    #     # 2.讲指定地区序列化器返回(需要将会地区下级地区进行嵌套的学历恶化)
    #     serializer = SubAreaSeializer(area)
    #
    #     return Response(serializer.data)


"""
设个根据id进行单个的查询
GenericAPIView--->>serializer_class
RetrieveAPIView---->>>queryset
RetieveAPIView
直接拼凑数据
"""


# GET /areas/
# class AreasView(GenericAPIView):
class AreasView(ListAPIView):
    # 指定序列化器类
    serializer_class = AreaSerializer

    # 指定当前视图所使用的查询集
    queryset = Area.objects.filter(parent=None)

    # def get(self, request):
    #     """获取所有升级地区的信息"""
    #     """
    #     1. 查询所有升级的信息
    #     2. 将省级地区的信息序列化并返回
    #     """
    #     #  1. 查询所有升级的信息
    #
    #     # 注意:这里不是用all进行查询啊,因为所有的数据都在一张表当中
    #
    #     # 只需要查询部分数据,因此需要用到过滤器
    #     # areas  = Area.objects.filter(parent=None)
    #
    #
    #     areas = self.get_queryset()
    #     # 这里有需要进行对数据的组织,不要忘了数据的烦序列化,很重要的哦
    #
    #     # 2. 将省级地区的信息序列化并返回
    #     # 注意:是多对象,必须使用manny
    #     serializer = self.get_serializer(areas, manny=True)
    #
    #     return Response(serializer.data)


"""
使用到了对象的拆分,马上思维惯性到序列化器

马上升级所继承的类
而且指定数据集的时候不一定是all,也可以filter进行过滤操作
由于查询的结果是多组数据,需要在对数据进行反序列化器的的时候,添加manny

对于查询的结果,其实也可以是使用queryset进行查询,在get方法当中
,利用get_queryset获取

其实我们可以从另一个角度进行思考,目的是查询所有<对所有数据限定产出>
listAPIView刚刚好

所以品拼凑ListAPIView,所需要的数据即可


"""
