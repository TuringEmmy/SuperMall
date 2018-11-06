# author    python
# time      18-11-4 上午10:31
# project   SuperMall

from rest_framework import serializers

from goods.models import SKU

# 商品搜索序列化器类
from drf_haystack.serializers import HaystackSerializer




# 商品sku序列化器
class SKUSerializer(serializers.ModelSerializer):
    """商品序列化器类"""

    class Meta:
        model = SKU

        fields = ('id', 'name', 'price', 'comments', 'default_image_url')



class SKUIndexSerializer(HaystackSerializer):
    """搜索结果序列化"""
    object =SKUSerializer(label='商品')

    class Meta:
        # 指定索引类
        from goods.search_indexes import SKUIndex
        index_classes  = [SKUIndex]

        fields = ('text', 'object')