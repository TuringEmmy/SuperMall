from celery import Celery

# 创建Celery类的实例对象
celery_app = Celery('celery_tasks')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 启动celery worker时自动发现任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])