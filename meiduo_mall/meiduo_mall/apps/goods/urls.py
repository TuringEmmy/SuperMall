# author    python
# time      18-10-31 下午7:46
# project   SuperMall
from django.conf.urls import url

from goods import views

urlpatterns=[
    url(r'categories/(?P<category_id>\d+)/skus/',views.SKUListView.as_view()),
]