# author    python
# time      18-10-30 下午7:33
# project   SuperMall
from django.conf.urls import url

from areas import views

urlpatterns=[
    url(r'^areas/$',views.AreasView.as_view()),
    url(r'^areas/(?P<pk>\d+)/$',views.SubAreasView.as_view()),
]