##### 1. 用户个人信息获取API

```http
API: GET /user/
参数:
	在请求头中传递jwt token数据
响应:
	{
		"id": "用户id",
        "username": "用户名",
        "mobile": "手机号",
        "email": "邮箱",
        "email_active": "邮箱验证标记"
	}
```

request对象有一个属性user(request.user):

​	如果用户认证成功，request.user就是登录的用户对象；

​	如果用户未经过认证，request.user是一个匿名用户类的对象。

​	前端在请求头中传递的jwt token数据之后，DRF框架中引入的JWT认证机制会校验jwt token的有效性，如果无效直接返回401认证错误。

##### 2. 登录用户邮箱设置API

```http
API: PUT /email/
参数:
	在请求头中传递jwt token数据
	{
        "email": "设置邮箱"
	}
响应:
	{
        "id": "用户id",
        "email": "邮箱"
	}
```

使用celery发送邮箱验证的邮件。

##### 3. 用户邮箱的验证API

设置用户的邮箱验证标记。

```http
API: PUT /emails/verification/?token=<token>
参数:
	通过查询字符串传递邮箱验证的token数据
响应:
	{
        "message": "OK"
	}
```

##### 4. 省市县地区三级联动

1）省市县数据的存储

地区表的某些数据之间存在一对多(一个省下面有多个市，一个市下面有多个县)关系，自关联。

| ID(地区ID) | name(地区名称) | parent_id(父级地区ID) |
| ---------- | -------------- | --------------------- |
| 200001     | 江苏省         | NULL                  |
|            |                |                       |
|            |                |                       |

2）Area地区模型类定义

```python
class Area(models.Model):
    """
    行政区划
    """
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True, verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'

    def __str__(self):
        return self.name
```

3）related_name选项参数的作用

```python
# 1. 查询ID`200001`对应地区的信息
area = Area.objects.get(id=200001) # 江苏省

# 2. 获取和江苏省关联的市的信息 
areas = area.area_set.all()

# 在模型类定义parent关联属性时，一旦指定了related_name='subs'之后，获取和一个地区关联的下级地区时，
# 直接使用下面语句
areas = area.subs.all()
```

##### 5. 省市县地区三级联动API

1）获取所有省级地区的信息

```http
API: GET /areas/
参数:
	无
响应:
	[
        {
            'id': '地区id',
            'name': '地区名称'
        },
        ...
	]
```

2）获取省级地区的下级市的信息

```http
API: GET /areas/(?P<pk>\d+)/
参数:
	在url地址中传递省id
响应:
	{
        'id': '省id',
        'name': '省名称',
        'subs': [
            {
                'id': '市id',
                'name': '市名称'
            },
            ...
        ]
	}
```

3）获取市级地区的下级县的信息

```http
API: GET /areas/(?P<pk>\d+)/
参数:
	在url地址中传递市id
响应:
	{
        'id': '市id',
        'name': '市名称',
        'subs': [
            {
                'id': '县id',
                'name': '县名称'
            },
            ...
        ]
	}
```



4）根据id获取指定地区的信息

```http
API: GET /areas/(?P<pk>\d+)/
参数:
	通过url地址传递地区id.
响应:
	根据id获取指定地区的信息，将指定的地区序列化并返回(把和地区关联的下级地区做嵌套序列化)
	{
        'id': '地区id',
        'name': '地区名称',
        'subs': [
            {
                'id': '下级地区id',
                'name': '下级地区name'
            },
            ...
        ]
	}
```













