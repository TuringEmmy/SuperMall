# author    python
# time      18-11-4 下午2:38
# project   SuperMall

from rest_framework.pagination import PageNumberPagination


class StandardResultPagination(PageNumberPagination):
    """自定义分类页"""

    # 指定默认页容量
    page_size = 6
    # 获取分页数据时传递也容量参数名称
    page_size_query_param = 'page_size'

    # 指定最大页容量
    max_page_size = 20