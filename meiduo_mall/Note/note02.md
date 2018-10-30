### 美多商城项目

##### 1. 用户数据表

```
用户名
密码
手机号
邮箱
是否是管理员
删除标记
```

##### 2. 用户注册业务

子业务:

​	1）短信验证码子业务

​	2）用户名是否重复

​	3）手机号是否重复

​	4）用户注册信息保存子业务

##### 3. 短信验证码API接口

功能: 获取短信验证码。

```http
URL: GET /sms_codes/(?P<mobile>1[3-9]\d{9})/
参数:
	通过url传递手机号<mobile>
响应: 
	{
        "message": "OK"
	}
```

##### 4. 域名

域名->网站IP

DNS解析->获取和网站域名对应IP地址

前端live-server服务器域名: `www.meiduo.site` 127.0.0.1

后端Django服务器域名: `api.meiduo.site` 127.0.0.1

本地域名设置:

通过域名访问一个网站时，浏览器在进行DNS解析之前，会到`/etc/hosts` 文件中查询域名和IP之间的对应关系，如果查到会直接访问对应IP，如果查不到才会进行DNS解析。

##### 5. 跨域请求

同源策略:

​	对于两个url地址，如果url地址的`协议`,`IP`和`PORT`完全一致，那么这两个地址就属于同源，否则就属于不同源。

浏览器在通过一个页面发起ajax请求时，如果发现源请求地址和被请求地址不是同源，浏览器就进行跨域请求。

`http://www.meiduo.site:8080/js/register.js`

`http://api.meiduo.site:8000/sms_codes/13155667788/`

浏览器在进行跨域请求时，会在请求头添加一个`Origin: 源请求地址`，被请求的服务器在返回响应时，如果允许源请求地址进行跨域请求，需要在响应头中添加一个`Access-Control-Allow-Origin: 源请求地址`，浏览器在收到响应时，如果发现响应中含有``Access-Control-Allow-Origin: 源请求地址`，则认为被请求服务器是允许源地址进行跨域请求，否则认为不允许，会直接报错。

##### 6. Celery异步任务队列

任务发送者，任务执行者，中间人

```python
安装: pip install celery

使用:
1）创建一个Celery类的实例对象
from celery import Celery
celery_app = Celery('demo')

2）进行配置，配置broker的地址
配置文件：broker_url = '中间人地址'

3）加载配置
celery_app.config_from_object('配置文件路径')

4）封装任务函数
@celery_app.task(name='my_first_task')
def task_func(a, b):
    print('任务函数被调用')
    # ...
 
5）创建worker
celery -A `celery_app对象包路径` worker -l info

6）发出要执行任务
task_func.delay(1, 3)
```

##### 补充

axios请求

```js
axios.get('url地址', [config])
    .then(response => {
    	// 请求成功，可通过response.data获取响应数据
	})
    .catch(error => {
    	// 请求失败，可通过error.response获取响应对象
    	// error.response.data获取响应数据
	})

axios.post('url地址', [data], [config])
    .then(response => {
    	// 请求成功，可通过response.data获取响应数据
	})
    .catch(error => {
    	// 请求失败，可通过error.response获取响应对象
    	// error.response.data获取响应数据
	})
```



