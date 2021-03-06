# author    python
# time      18-11-3 下午5:29
# project   SuperMall
import os
from collections import OrderedDict
import time

from django.conf import settings

from contents.models import ContentCategory
from goods.models import GoodsChannel


def generate_static_index_html():
    """生成静态化首页的index.html"""
    # 从数据库查询出首页所需的商品分类数据和广告数据
    print('%s: generate_static_index_html' % time.ctime())
    # 商品频道及分类菜单
    # 使用有序字典保存类别的顺序
    # categories = {
    #     1: { # 组1
    #         'channels': [{'id':, 'name':, 'url':},{}, {}...],
    #         'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
    #     },
    #     2: { # 组2
    #
    #     }
    # }
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:
        group_id = channel.group_id  # 当前组

        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        cat1 = channel.category  # 当前频道的类别

        # 追加当前频道
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })
        # 构建当前类别的子类别
        for cat2 in cat1.goodscategory_set.all():
            cat2.sub_cats = []
            for cat3 in cat2.goodscategory_set.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)

    # 广告内容
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        # 表里面的多余字段key是和id对应的，在这里市委了方便查询，在表格里面多添加的
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')



    #   使用index.html模板文件，进模板渲染，湖区选人啊数据
    context = {
        'categories': categories,
        'contents': contents
    }
    # render()在这里返回HttpResponse
    # 渲染模板，获取模板的文件，获取模板对象
    from django.template import loader
    # temp = loader.get_template('index.html')
    temp = loader.get_template('index.html')

    # 模板的渲染：给模板文件传递数据，将模板文件的变量进行替换，获取替换之后的内容
    res_html = temp.render(context)

    # 将渲染之后的html页面内容保存成一个静态文件
    save_path =os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR,'index.html')
    with open(save_path,'w',encoding='utf-8') as f:
        f.write(res_html)



