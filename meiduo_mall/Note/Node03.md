### 一、用户功能

1. #### 用户名和手机号码是否重复

#### 后端接口设计：

**请求方式**： GET `usernames/(?P\w{5,20})/count/`

**请求参数**： 路径参数

| 参数       | 类型   | 是否必传 | 说明   |
| -------- | ---- | ---- | ---- |
| username | str  | 是    | 用户名  |

**返回数据**： JSON

```json
{
    "username": "itcast",
    "count": "1"
}
```

| 返回值      | 类型   | 是否必须 | 说明   |
| -------- | ---- | ---- | ---- |
| username | str  | 是    | 用户名  |
| count    | int  | 是    | 数量   |

#### 后端接口设计：

**请求方式**： GET `mobiles/(?P1[3-9]\d{9})/count`

**请求参数**： 路径参数

| 参数     | 类型   | 是否必须 | 说明   |
| ------ | ---- | ---- | ---- |
| mobile | str  | 是    | 手机号  |

**返回数据**： JSON

```json
{
    "mobile": "18512345678",
    "count": 0
}
```

| 返回值    | 类型   | 是否必须 | 说明   |
| ------ | ---- | ---- | ---- |
| mobile | str  | 是    | 手机号  |
| count  | int  | 是    | 数量   |

2. #### 注册用户信息的保存(后端API序列化器)

**请求方式**： POST `/users/`

**请求参数**： JSON 或 表单

| 参数名       | 类型   | 是否必须 | 说明       |
| --------- | ---- | ---- | -------- |
| username  | str  | 是    | 用户名      |
| password  | str  | 是    | 密码       |
| password2 | str  | 是    | 确认密码     |
| sms_code  | str  | 是    | 短信验证码    |
| mobile    | str  | 是    | 手机号      |
| allow     | str  | 是    | 是否同意用户协议 |

**返回数据**： JSON

```json
{
    "id": 9,
    "username": "python8",
    "mobile": "18512345678",
}
```

| 返回值      | 类型   | 是否必须 | 说明   |
| -------- | ---- | ---- | ---- |
| id       | int  | 是    | 用户id |
| username | str  | 是    | 用户名  |
| mobile   | str  | 是    | 手机号  |



3. #### 注册用户信息的保存(后盾API基本业务逻辑)

使用CreateAPIView来实现，并使用序列化器`CreateUserSerializer`





4. #### 注册用户信息的保存(前端vue的逻辑)

```js
if(this.error_name == false && this.error_password == false && this.error_check_password == false
                && this.error_phone == false && this.error_sms_code == false && this.error_allow == false) {
                axios.post(this.host + '/users/', {
                        username: this.username,
                        password: this.password,
                        password2: this.password2,
                        mobile: this.mobile,
                        sms_code: this.sms_code,
                        allow: this.allow.toString()
                    }, {
                        responseType: 'json'
                    })
                    .then(response => {
                        location.href = '/index.html';
                    })
                    .catch(error=> {
                        if (error.response.status == 400) {
                            if ('non_field_errors' in error.response.data) {
                                this.error_sms_code_message = error.response.data.non_field_errors[0];
                            } else {
                                this.error_sms_code_message = '数据有误';
                            }
                            this.error_sms_code = true;
                        } else {
                            console.log(error.response.data);
                        }
                    })
            }
        }
```



### 二、JWT认证机制

1. #### session认证存在的问题

#### 基于session认证所显露的问题

**Session**: 每个用户经过我们的应用认证之后，我们的应用都要在服务端做一次记录，以方便用户下次请求的鉴别，通常而言session都是保存在内存中，而随着认证用户的增多，服务端的开销会明显增大。

**扩展性**: 用户认证之后，服务端做认证记录，如果认证的记录被保存在内存中的话，这意味着用户下次请求还必须要请求在这台服务器上,这样才能拿到授权的资源，这样在分布式的应用上，相应的限制了负载均衡器的能力。这也意味着限制了应用的扩展能力。

**CSRF**: 因为是基于cookie来进行用户识别的, cookie如果被截获，用户就会很容易受到跨站请求伪造的攻击。

2. #### jwt token数据可视化

jwt流程上是这样的：

- 用户使用用户名密码来请求服务器
- 服务器进行验证用户的信息
- 服务器通过验证发送给用户一个token
- 客户端存储token，并在每次请求时附送上这个token值
- 服务端验证token值，并返回数据

这个token必须要在每次请求时传递给服务端，它应该保存在请求头里， 另外，服务端要支持`CORS(跨来源资源共享)`策略，一般我们在服务端这么做就可以了`Access-Control-Allow-Origin: *`

##### **header**

jwt的头部承载两部分信息：

- 声明类型，这里是jwt
- 声明加密的算法 通常直接使用 HMAC SHA256

完整的头部就像下面这样的JSON：

```json
{
  'typ': 'JWT',
  'alg': 'HS256'
}
```

##### **payload**

载荷就是存放有效信息的地方。这个名字像是特指飞机上承载的货品，这些有效信息包含三个部分

- 标准中注册的声明
- 公共的声明
- 私有的声明

**标准中注册的声明** (建议但不强制使用) ：

- **iss**: jwt签发者
- **sub**: jwt所面向的用户
- **aud**: 接收jwt的一方
- **exp**: jwt的过期时间，这个过期时间必须要大于签发时间
- **nbf**: 定义在什么时间之前，该jwt都是不可用的.
- **iat**: jwt的签发时间
- **jti**: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。

**公共的声明** ： 公共的声明可以添加任何的信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可解密.

**私有的声明** ： 私有声明是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息。

定义一个payload:

```
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```

##### **signature**

JWT的第三部分是一个签证信息，这个签证信息由三部分组成：

- header (base64后的)
- payload (base64后的)
- secret

这个部分需要base64加密后的header和base64加密后的payload使用`.`连接组成的字符串，然后通过header中声明的加密方式进行加盐`secret`组合加密，然后就构成了jwt的第三部分。

```
// javascript
var encodedString = base64UrlEncode(header) + '.' + base64UrlEncode(payload);

var signature = HMACSHA256(encodedString, 'secret'); // TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```

> secret是保存在服务器端的，jwt的签发生成也是在服务器端的，secret就是用来进行jwt的签发和jwt的验证，所以，它就是你服务端的私钥，在任何场景都不应该流露出去。一旦客户端得知这个secret, 那就意味着客户端是可以自我签发jwt了。

![TuringEmmy201810271540626254](image/TuringEmmy201810271540626254.png)



3. #### jwt token使用注意点


**优点**

- 因为json的通用性，所以JWT是可以进行跨语言支持的，像JAVA,JavaScript,NodeJS,PHP等很多语言都可以使用。
- 因为有了payload部分，所以JWT可以在自身存储一些其他业务逻辑所必要的非敏感信息。
- 便于传输，jwt的构成非常简单，字节占用很小，所以它是非常便于传输的。
- 它不需要在服务端保存会话信息, 所以它易于应用的扩展

> 不应该在jwt的payload部分存放敏感信息，因为该部分是客户端可解密的部分。
>
> 保护好secret私钥，该私钥非常重要。
>
> 如果可以，请使用https协议


4. #### 注册成功签发jwt token数据


**安装配置**`pip install djangorestframework-jwt`

并在setting当中进行设置

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),				# 指明token的有效期
}
```

Django REST framework JWT 扩展的说明文档中提供了手动签发JWT的方法

```python
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

payload = jwt_payload_handler(user)
token = jwt_encode_handler(payload)
```

在注册成功后，连同返回token，需要在注册视图中创建token。

修改CreateUserSerializer序列化器，在create方法中增加手动创建token的方法

### 三、用户功能

1. #### 注册用户信息的保存


**前端保存token**

- **sessionStorage** 浏览器关闭即失效
- **localStorage** 长期有效

使用方法

```python
sessionStorage.变量名 = 变量值   // 保存数据
sessionStorage.变量名  // 读取数据
sessionStorage.clear()  // 清除所有sessionStorage保存的数据
localStorage.变量名 = 变量值   // 保存数据
localStorage.变量名  // 读取数据
localStorage.clear()  // 清除所有localStorage保存的数据
```


2. #### 用户登录(后端API-jwt扩展登录视图使用)


**请求方式**： POST `/authorizations/`

**请求参数**： JSON 或 表单

| 参数名      | 类型   | 是否必须 | 说明   |
| -------- | ---- | ---- | ---- |
| username | str  | 是    | 用户名  |
| password | str  | 是    | 密码   |

**返回数据**： JSON

```
{
    "username": "python",
    "user_id": 1,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VybmFtZSI6InB5dGhvbjgiLCJleHAiOjE1MjgxODI2MzQsImVtYWlsIjoiIn0.ejjVvEWxrBvbp18QIjQbL1TFE0c0ejQgizui_AROlAU"
}

```

| 返回值      | 类型   | 是否必须 | 说明     |
| -------- | ---- | ---- | ------ |
| username | str  | 是    | 用户名    |
| user_id  | int  | 是    | 用户id   |
| token    | str  | 是    | 身份认证凭据 |




3. #### 用户登录(后端API-自定义jwt扩展登录视图响应数据函数)


在users/utils.py 中，创建

```python
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }
```

修改配置文件

```python
# JWT
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}
```

但是有些时候为了用户名和手机号都能登陆

**修改Django认证系统的认证后端需要继承django.contrib.auth.backends.ModelBackend，并重写authenticate方法。**

`authenticate(self, request, username=None, password=None, **kwargs)`方法的参数说明：

- request 本次认证的请求对象
- username 本次认证提供的用户账号
- password 本次认证提供的密码

重写authenticate方法的思路：

1. 根据username参数查找用户User对象，username参数可能是用户名，也可能是手机号
2. 若查找到User对象，调用User对象的check_password方法检查密码是否正确





4. #### 用户登录(前端vue逻辑)




5. #### 用户登陆(自定义Django认证后端类)

