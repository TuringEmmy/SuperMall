# author    python
# time      18-10-28 下午3:45
# project   SuperMall
from django.conf.urls import url

from oauth import views

urlpatterns=[
    url(r'qq/authorization/$',views.QQAuthURLView.as_view())
]