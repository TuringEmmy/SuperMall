### 美多商城项目

##### 1. QQ登录-效果

使用QQ进行第三方登录时，当QQ用户授权登录之后，先判断QQ用户是否绑定过本网站的用户，如果没有绑定过，就让用户进行绑定，如果已经绑定过，直接让对应的用户登录成功。

##### 2. QQ登录-准备工作

1）注册QQ开发者账户

2）创建开发者应用，并提交配置信息，等待审核

3）审核通过，获取appid和app_key，然后就可以进行开发。

##### 3. QQ登录-开发关键点

获取QQ登录用户的openid(`QQ用户的唯一身份标识`)，然后根据openid进行处理，如果openid绑定过本网站用户，直接登录成功，如果openid没有绑定过本网站用户，先让用户进行绑定操作。

一个用户可以绑定多个QQ账户。

| id   | user_id | openid                 |
| ---- | ------- | ---------------------- |
| 1    | 2       | QKKSIDIOD8183838DKKDK  |
| 2    | 2       | QKKDIK188idiKDODLDLLDL |
|      |         |                        |

##### 4. QQ登录-API接口分析

1）获取QQ登录网址API。

```http
API: GET /oauth/qq/authorization/?next=<登录跳转地址>
参数:
	通过查询字符串传递QQ登录成功之后跳转页面地址
响应:
	{
        "login_url": "QQ登录网址"
	}
```

2）获取QQ登录用户openid并进行处理API.

```http
API: GET /oauth/qq/user/?code=<code>
参数:
	通过查询字符串传递code
响应:
	根据code最终获取QQ登录用户的openid，然后根据openid进行处理
	1）如果openid已经绑定过本网站用户，直接生成jwt token并返回
        {
            "user_id": "用户id",
            "username": "用户名",
            "token": "jwt token数据"
        }
    2）如果openid未绑定过本网站用户，返回openid(对openid进行加密)
    	{
            "access_token": "openid加密内容"
    	}
```

3）保存绑定QQ用户的身份信息API.

```http
API: POST /oauth/qq/user/
参数:
	{
        "mobile": "手机号",
        "password": "密码",
        "sms_code": "短信验证码",
        "access_token": "openid加密内容"
	}
响应:
	{
        "id": "用户id",
        "username": "用户名",
        "token": "jwt token数据"
	}
```