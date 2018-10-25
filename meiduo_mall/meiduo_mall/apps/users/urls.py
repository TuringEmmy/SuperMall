# author    python
# time      18-10-25 下午9:24
# project   SuperMall
from django.conf.urls import url

from users import views

urlpatterns=[
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.UsernameCountView.as_view()),
]

