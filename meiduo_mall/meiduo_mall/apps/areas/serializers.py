# author    python
# time      18-10-30 下午8:08
# project   SuperMall

from rest_framework import serializers

from areas.models import Area


class AreaSerializer(serializers.ModelSerializer):
    """
    地区序列化器类
    """

    class Meta:
        model = Area
        fields = ('id', 'name')
