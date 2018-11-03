##### 1. 历史浏览记录

1）什么时候需要添加用户的历史浏览记录？

答：当登录用户访问某个商品的详情页面时，需要添加历史浏览记录。

2）添加历史浏览记录时，需要保存哪些数据？

答: 商品id。

3）历史浏览记录数据保存在哪里？

答: 用户可能频繁浏览商品，为了防止频繁操作mysql数据库，可以将浏览记录存储在redis中。

4）采用redis中哪种数据类型？

答: history_<user_id>: [1, 5, 3]

```
string: 字符串  key: value
	history_<user_id>: '1,2,5'

hash: 哈希  key: {'field': 'value', ...}
	history: {
        history_<user_id>: '1,2,5',
        ...
	}
	
list: 列表
	history_<user_id>: [3, 1, 2, 5]

set: 无序集合
	pass

zset: 有序集合
	权重
```

5）添加用户浏览记录的流程？

```
去重: 如果用户已经浏览过该商品，将该商品的sku_id从list列表中移除
左侧加入: 保持浏览顺序
截取: 只保留最新的几个浏览记录
```

##### 2. 历史浏览记录添加API

```http
API: POST /browse_histories/
参数:
	通过请求头传递jwt token
	{
        "sku_id": "商品id"
	}
响应:
	{
        "sku_id": "商品id"
	}
```

lrem(key, count, value): 

​	从redis列表中移除元素，有则移除，无则忽略

lpush(key, *values): 

​	向redis列表中左侧加入元素

ltrim(key, start, stop): 

​	保留redis列表指定区间内的元素

##### 3. 历史浏览记录的获取

```http
API: GET /browse_histories/
参数:
	通过请求头传递jwt token
响应:
	[
        {
           "id": "商品id",
           "name": "商品名称",
           "price": "商品价格",
           "comments": "商品评论量",
           "default_image_url": "默认图片"
        },
        ...
	]
```

lrange(key, start, stop): 

​	获取redis列表指定区间内的元素

##### 4. 获取第三级分类SKU商品的数据API

根据一个第三级分类id，获取该分类下的SKU商品的数据，支持分页和排序。

```http
API: 
GET /categories/(?P<category_id>\d+)/skus/?page=<页码>&page_size=<页容量>&ordering=<排序字段>
参数:
	通过url传递第三级分类ID
	通过查询字符串传递页码，页容量和排序字段
响应:
	{
        "count": 14,
        "next": "http://api.meiduo.site:8000/categories/115/skus/?page=2",
        "previous": null,
        "results": [
            {
                "id": "商品id",
                "name": "商品名称",
                "price": "价格",
                "default_image_url": "默认图片",
                "comments": "评论量"
            },
            ...
        ]
	}
```

1）获取第三级分类ID所有SKU商品信息。

2）设置分页和排序。

##### 5. 商品搜索

关键字: iPhone

需求:

​	根据商品的名称和副标题搜索商品的信息。

```bash
select * from tb_sku where name like '%iPhone%' or caption like '%iPhone%';
```

在数据库的查询语句中，like语句查询效率很低。

1）搜索引擎

原理:

​	搜索引擎可以将数据表中存储的数据进行处理，建立一份索引结构的数据(`记录着索引数据和表数据之间对应的关系`)；

​	搜索引擎在建立索引数据时，会将`索引字段`的内容进行关键词拆分，然后还会记录某个关键词在哪些索引记录中存在。

​      索引字段: 通过哪些字段进行搜索，索引字段中就包含哪些内容。

2）haystack全文检索框架对接es搜索引擎

​	python中的一个全文检索框架，支持多种搜索引擎。es slor whoosh

​	帮助开发者使用搜索引擎的功能。

​	2.1 帮助开发者利用搜索引擎对数据表的数据建立索引数据。

​	2.2 帮助开发者利用搜索引擎进行关联词搜索，获取对应索引数据。

​	2.3 利用获取到的索引数据查询数据库中数据表，获取对应搜索结果。

##### 6. haystack全文检索框架对接es搜索引擎

1）建立索引数据

​	1.1 定义索引类

​	1.2 指定索引字段内容

​	  1.3 建立索引  `python manage.py rebuild_index`

2）编写搜索视图