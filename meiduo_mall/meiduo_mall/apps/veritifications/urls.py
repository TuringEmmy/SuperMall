# author    python
# time      18-10-25 下午3:59
# project   SuperMall
from django.conf.urls import url

from veritifications import views

urlpatterns=[
    url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
]