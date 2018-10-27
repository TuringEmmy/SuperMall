### 一、框架搭建

**创建数据库**

```python
create database shopMall default charset=utf8;
```

为本项目创建数据库用户（不再使用root账户）

```python
create user turing identified by 'mysql';
grant all on shopMall.* to 'turing'@'%';
flush privileges;
```

说明：

- 第一句：创建用户账号 meiduo, 密码 meiduo (由identified by 指明)
- 第二句：授权shopMall数据库下的所有表（shopMall.*）的所有权限（all）给用户turing在以任何ip访问数据库的时候（'turing'@'%'）
- 第三句：刷新生效用户权限

配置文件设置如下：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "shopMall",
        "HOST":"127.0.0.1",
        "PORT":'3306',
        "USER":"turing",
        "PASSWORD":'mysql',
    }
}
```

安装` 'rest_framework',`

**redis的配置**

安装django-redis，并配置

```
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.211.55.5:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.211.55.5:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"
```

**异常处理**对应utils包下的exceptions.py



### 二、用户功能



### 三、短信发送



### 四、域名设置



### 五、CORS跨域请求



### 六、异步任务

1. #### 跨域请求



2. #### 跨域请求的设置



3. #### 短信发送API接口问题

#### 

4. #### celery异步任务队列



5. #### celery的使用



6. #### celery发送短信











