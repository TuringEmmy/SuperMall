# author    python
# time      18-11-4 上午10:31
# project   SuperMall

from rest_framework import serializers

from goods.models import SKU


class SKUSerializer(serializers.ModelSerializer):
    """商品序列化器类"""
    class Meta:
        model = SKU

        fields = ('id','name','price','comments','default_image_url')