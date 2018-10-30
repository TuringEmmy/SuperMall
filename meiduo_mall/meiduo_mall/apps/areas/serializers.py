# author    python
# time      18-10-30 下午8:08
# project   SuperMall

from rest_framework import serializers

from areas.models import Area



# 获取省的序列化
class AreaSerializer(serializers.ModelSerializer):
    """
    地区序列化器类
    """

    class Meta:
        model = Area
        fields = ('id', 'name')



# 获取市和县的序列化

class SubAreaSeializer(serializers.ModelSerializer):

    # 使用序列化:使用指定的序列化
    subs = AreaSerializer(label='下级地区',many=True)
    class Meta:
        model = Area
        fields =('id','name','subs')

"""
注意:这里使用到了嵌套序列化,这个方法甚是巧妙
"""