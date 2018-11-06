# author    python
# time      18-11-4 下午4:36
# project   SuperMall


from haystack import indexes

# 索引类名称：<模型类>+Index
from goods.models import SKU


class SKUIndex(indexes.SearchIndex,indexes.Indexable):
    """商品的索引类"""
    # document=True说明此字段是索引字段
    # use_template=True说明简历索引数据时索引字段中包含那些内容会在一个文件中进行指定
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        """返回索引对应的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回需要角暗里索引数据的查询集"""
        return self.get_model().objects.filter(is_launched=True)