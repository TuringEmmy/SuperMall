import os

from celery import Celery



# 设置django所运行的环境
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings")

# 创建Celery类的实例对象
celery_app = Celery('celery_tasks')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 启动celery worker时自动发现任务
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_task.email'])

# 注意:这里有一个大坑,进行邮箱的发送的时候,使用到了setting,因此,这个main的模块需要进行django的环境设置