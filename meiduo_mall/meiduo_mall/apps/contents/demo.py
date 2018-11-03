# author    python
# time      18-11-3 下午6:15
# project   SuperMall
# 测试首页的静态生成
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")

import django
django.setup()



from contents.crons import generate_static_index_html

generate_static_index_html()