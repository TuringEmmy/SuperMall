# author    python
# time      18-10-30 下午6:01
# project   SuperMall


# 封装发送邮箱验证的邮件
from django.conf import settings
from django.core.mail import send_mail
# 奥入使用夺金称的celery_app
from celery_tasks.main import celery_app


# 对线面的函数进行小装饰
@celery_app(name='send_verify_email')
def send_verify_email(email,verify_url):
    subject = "美多商城邮箱验证"

    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
    send_mail(subject, "", settings.EMAIL_FROM, [email], html_message=html_message)