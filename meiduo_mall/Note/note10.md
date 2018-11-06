##### 1. 购物车数据的存储

需求：

​	登录用户和未登录用户都可以进行购物车记录添加。

`登录用户的购物车记录存储`:

1）登录用户的购物车记录存储在哪里?

答：用户可能频繁进行购物车记录添加和操作，为了防止频繁的操作mysql数据库，可以将购物车记录存储到redis中。

2）存储购物车记录时需要存储哪些数据？

答：`商品id`: `商品数量count`，`购物车记录勾选状态`

3）采用redis中哪种数据类型进行存储？

答：

```python
# hash  key: {'<field>': '<value>', ...}
# 使用hash存储用户购物车中添加的商品的id和对应的数量count
cart_<user_id>:{
    '<sku_id>': '<count>',
    '<sku_id>': '<count>',

}
```
    
# 使用set存储用户购物车中被勾选的商品的id
cart_selected_<user_id>: ('<sku_id>', '<sku_id>', ...)
    
# 例如，某用户的购物车记录如下:
cart_2 : {
    '1': '3',
    '3': '2',
    '5': '1'
}
    
cart_selected_2: ('1', '5')
    
id为2的用户购物车数据:
    id为1的商品添加了3件
    id为3的商品添加了2件
    id为5的商品添加了1件
	id为1和id为5的商品对应购物车记录是被勾选的。
```

`未登录用户的购物车记录存储`:	

未登录用户的购物车记录，为了防止过多占用服务器存储空间，所以不在服务器端进行存储，而是存储在客户端浏览器。

cookie存储未登录用户的购物车记录。

```python
{
    '<sku_id>': {
        'count': '<count>',
        'selected': '<selected>
    },
    ...
}

# 例如，未登录用户的购物车记录如下:
{
    1: {
        'count': 2,
        'selected': True
    },
    6: {
        'count': 1,
        'selected': False
    }
}

当前未登录用户的购物车添加了2条记录:
    id为1的商品添加了2件
    id为6的商品添加了1件
  	id为1的商品对应购物车记录是被勾选的。
```

`设置cookie`：

​	创建一个响应对象: response

​	response.set_cookie(<key>, <value>, max_age=<过期时间: s>)

`获取cookie`:

​	request.COOKIES: 保存客户端发送给服务器cookie数据

​	request.COOKIES.get(<key>)

`json模块`:

​	json.dumps(dict): 将python字典转换为json字符串数据;

​	json.loads(json_str)：将json字符串转换为python字典;

`pickle模块`：

​	pickle.dumps(obj): 将obj对象转换为bytes字节流。

​	pickle.loads(bytes字节流)：将bytes字节流转换为obj对象。	

`base64模块`:

​	base64.b64encode(bytes字节流): 将传入的bytes字节流数据进行base64编码，返回编码之后bytes内容

​	base64.b64decode(编码之后bytes字节流|字符串)：将传入的数据进行base64解码，返回解码之后的bytes内容

`设置cookie中购物车数据`:

​	cart_data = base64.b64encode(pickle.dumps(cart_dict)).decode()

​	response.set_cookie('cart',  cart_data, max_age='过期时间')

`解析cookie中的购物车数据`:

​	cookie_cart = request.COOKIES.get('cart')

​	cart_dict = pickle.loads(base64.b64decode(cart_data))

##### 2. 购物车记录添加API

```http
API: POST /cart/
参数:
	通过请求头传递jwt token数据
	{
        "sku_id": "商品id",
        "count": "商品数量",
        "selected" : "勾选状态", # 可以不传，默认为勾选
	}
响应:
	{
        "sku_id": "商品id",
        "count": "商品数量",
        "selected": "勾选状态"
	}
```

##### 3. 购物车记录获取API

```http
API: GET /cart/
参数:
	通过请求头传递jwt token数据
响应:
	[
        {
            "id": "商品id",
            "name": "商品名称",
            "price": "商品价格",
            "default_image_url": "默认图片",
            "count": "购物车商品数量",
            "selected": "勾选状态"
        },
        ...
	]
```

##### 4. 购物车记录修改API

```http
API: PUT /cart/
参数:
	通过请求头传递jwt token数据
	{
        "sku_id": "商品id",
        "count": "修改数量结果",
        "selected": "勾选状态", # True: 选中 Flask: 不选中
	}
响应:
	{
        "sku_id": "商品id",
        "count": "修改数量结果",
        "selected": "勾选状态"
	}
```

##### 5. 购物车记录删除API

```http
API: DELETE /cart/
参数:
	通过请求头传递jwt token数据
	{
        "sku_id": "商品id"
	}
响应:
	{
        "sku_id": "商品id"
	}
```

##### 6. redis操作命令

`hash命令`:

hincrby(key, field, count): 

​	给hash中指定属性field的值累加count，如果属性和值不存在，会新建属性和值。

hgetall(key): 

​	获取hash中所有属性和值。

hset(key, field, value): 

​	将hash中指定属性field值设置为value。

hdel(key, *fields): 

​	删除hash中指定属性和值，如果属性不存在，直接忽略。

`set命令`:

sadd(key, *members):

​	向set集合中添加元素，集合中元素是唯一的。

smembers(key): 

​	获取set中所有元素。

srem(key, *members): 

​	从set集合中移除元素，有则移除，无则忽略。