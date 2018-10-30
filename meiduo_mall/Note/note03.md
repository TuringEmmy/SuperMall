### 美多商城项目

##### 1. 用户名是否重复API

获取用户名的数量。

```http
API: GET /usernames/(?P<username>\w{5,20})/count/
参数:
	通过url地址传递用户名
响应:
	{
       	"username": "<username>",
       	"count": "<count>"
	}
```

##### 2. 手机是否重复API

```http
API: GET /mobiles/(?P<mobile>1[3-9]\d{9})/count/
参数:
	通过url地址传递手机号
响应:
	{
       	"mobile": "<mobile>",
       	"count": "<count>"
	}
```

##### 3. 用户注册信息保存API

创建新用户。

```http
API: POST /users/
参数:
	{
        "username": "用户名",
        "password": "密码",
        "password2": "重复密码",
        "mobile": "手机号",
        "sms_code": "短信验证码",
        "allow": "是否同意协议"
	}
响应:
	{
        "id": "用户id",
        "username": "用户名",
        "mobile": "手机号"
	}
```

##### 4. jwt 认证机制

1）session认证机制

```python
1. 接收用户名和密码
2. 校验用户名和密码是否正确
3. 在session保存登录用户的信息
	session['user_id'] = 2
	session['username'] = 'smart'
4. 返回应答
```

基于session认证机制所存在问题：

a）session信息存储在服务器，如果登录用户过多，会占用很多服务器空间。

b）session依赖cookie，客户端session信息的标识保存在cookie中，可能会产生cookie被拦截，造成CSRF攻击(跨站请求伪造)。

2）jwt认证机制(替代session认证机制)

```
1. 接收用户名和密码
2. 校验用户名和密码是否正确
3. 由服务器生成(签发)一个jwt token的字符串(该字符串中保存了登录用户的信息)
	服务器 -> 公安局  jwt token -> 身份证
4. 返回应答，将jwt token字符串返回给客户端
```

​	客户端需要保存jwt token，并且在之后请求服务器时，如果需要服务器进行身份验证，需要携带jwt token数据，由服务器验证jwt token数据有效性。

3）jwt token数据组成

jwt token是一个字符串，由3部分组成，用`.`隔开。

header: 头部

```
{
    'token类型',
    '加密算法'
}
```

使用base64对头部信息进行base64加密，加密之后生成字符串就是header，base64加密很容易被解密。

payload: 载荷。

保存有效数据。

```python
{
    'id': '用户id',
    'username': '用户名',
    'email': '邮箱',
    ...
    'exp': 'token有效时间'
}
```

使用base64对载荷信息进行base64加密，加密之后生成字符串就是payload。

signature: 签名。

防止jwt token数据被伪造。

签名是由服务器将`header`和`payload`拼接，用`.`隔开，然后使用一个密钥(secret_key)对拼接后的字符串进行加密，加密之后的内容就是signature。

```
header:
	{
        'jwt',
        '算法'
	}

payload:
	{
        'id': 2,
        'username': 'smart',
        ...
        'exp': 'token有效时间'
	}
	
假如服务器密钥为: 123abc
signature:
	
```

##### 5. 用户登录API

```http
API: POST /authorizations/
参数:
	{
        "username": "用户名",
        "password": "密码"
	}
响应:
	{
        "user_id": "用户id",
        "username": "用户名",
        "token": "jwt token数据"
	}
```

jwt 扩展中提供了一个登录视图，就是接收username和password，然后校验账户密码正确之后，会签发jwt token数据并返回。

1）自定义jwt 扩展的登录视图响应数据函数

```python
def jwt_response_payload_handler(token, user=None, request=None):
    """自定义jwt扩展响应数据函数"""
    return {
        'user_id': user.id,
        'username': user.username,
        'token': token
    }

# 配置
JWT_AUTH = {
    ...
    # 设置jwt扩展登录视图响应数据函数
    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'users.utils.jwt_response_payload_handler',
}
```

2）登录账户支持用户名和手机号

jwt扩展的登录视图没有自己实现账户和密码的验证代码，而是调用Django认证系统中一个方法`authenticate`进行账户和密码的验证。

```python
obtain_jwt_token
-> from django.contrib.auth import authenticate
-> from django.contrib.auth.backends import ModelBackend
   (ModelBackend类中有一个方法叫authenticate, 此方法实现账户和密码校验代码，默认账户仅支持用户名)
```

自定义Django的认证后端类:

```python
class UsernameMobileAuthBackend(ModelBackend):
	 def authenticate(self, request, username=None, password=None, **kwargs):
     	"""重写父类authenticate方法，让登录账户同时支持用户名和手机号"""
        ...
```

设置Django认证后端配置项：

```python
# 默认配置项
# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBackend']
```