# author    python
# time      18-11-2 下午5:02
# project   SuperMall


import os
from fdfs_client.client import Fdfs_client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")

client = Fdfs_client('./client.conf')

# client = Fdfs_client('/home/python/Desktop/SuperMall/meiduo_mall/meiduo_mall/utils/fastdfs/client.conf')
# ret = client.upload_by_filename('/home/python/Desktop/SuperMall/meiduo_mall/meiduo_mall/utils/fastdfs/test_pic.jpg')

ret = client.upload_by_filename('test_pic.jpg')

print(ret)



