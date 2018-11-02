# author    python
# time      18-11-2 下午5:52
# project   SuperMall


# 重写FileSystemStorage类里面的方法
from fdfs_client.client import Fdfs_client

from django.core.files.storage import Storage

from django.conf import settings


# =======================重写这个干函数,返回什么值,什么久保存到FDFS里面
class FDFStorage(Storage):
    """FDFS文件存储类"""

    def _save(self, name, content):
        """
        :param name: 双传文件的名称 test_pic.jpg
        :param content: 包含红素昂穿文件内容的File对象,可以通过conten.read()获取文件内容
        :return:
        """

        client = Fdfs_client(settings.FDFS_CLIENT_CONF)

        # 上传文件到FDFS文件存储系统
        res = client.upload_by_buffer(content.read())

        if res.get("Status") != 'Upload successed.':
            raise Exception("文件上传到FDFS系统失败")

        # 获取文件的id
        file_id = res.get("Remote file_id")

        return file_id

    def exists(self, name):
        """
        django框架调用文件存储类中的_save进行文件保存之前,会县调用exist方法判断文件按名在文件存储系统是否重复
        :param name: 上传文件的名称
        :return:
        """

        # 注意:这个文件名永远不会重复

        return False


    def url(self, name):
        """
        返回可访问的文件存储系统中文件系统的url地址
        :param name: 表中图片字段存储内容(文件id)
        :return:
        """
        return settings.FDFS_URL+name
