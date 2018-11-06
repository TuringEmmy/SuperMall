# author    python
# time      18-10-31 下午7:46
# project   SuperMall
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from goods import views

urlpatterns = [
    url(r'categories/(?P<category_id>\d+)/skus/', views.SKUListView.as_view()),
]

# router = DefaultRouter()
# router.register('skus/search/', views.SKUSearchViewSet, base_name='skus_search')
#
# urlpatterns += router.urls


router = DefaultRouter()
router.register('skus/search', views.SKUSearchViewSet, base_name='skus_search')
urlpatterns += router.urls


# 注意路由：添加/就无法找到