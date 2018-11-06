# author    python
# time      11/5/18 5:36 PM
# project   SuperMall
from django.conf.urls import url

from cart import views

urlpatterns=[
    url(r'^cart/$',views.CartView.as_view()),
]