import base64

from django.test import TestCase
import pickle


# Create your tests here.
# 测试字典转换春耕字符串的方法
def object_convert_into_string():
    # pickle.dumps(obj) :将对象转换为bytes
    personal_dict = {
        1: {
            'name': 'turing',
            'age': 23
        },
        2: {
            'name': 'ouyang',
            'age': 26
        },

    }

    personal_data = pickle.dumps(personal_dict)

    print(personal_data)


def string_convert_into_object():
    personal_data = b'\x80\x03}q\x00(K\x01}q\x01(X\x04\x00\x00\x00nameq\x02X\x06\x00\x00\x00turingq\x03X\x03\x00\x00\x00ageq\x04K\x17uK\x02}q\x05(h\x02X\x06\x00\x00\x00ouyangq\x06h\x04K\x1auu.'

    personal_dict = pickle.loads(personal_data)
    print(personal_dict)


# =============================使用base64模块==========================
def object_convert_string_by_base64():
    personal_data = b'\x80\x03}q\x00(K\x01}q\x01(X\x04\x00\x00\x00nameq\x02X\x06\x00\x00\x00turingq\x03X\x03\x00\x00\x00ageq\x04K\x17uK\x02}q\x05(h\x02X\x06\x00\x00\x00ouyangq\x06h\x04K\x1auu.'

    personal_data = base64.b64encode(personal_data)
    print(personal_data)
    result = personal_data.decode()
    print(result)
    # =================一步到位=================
    res = base64.b64encode(pickle.dumps(result)).decode()
    print(res)


def jiexi():
    peronal_data = 'gANYaAAAAGdBTjljUUFvU3dGOWNRRW9XQVFBQUFCdVlXMWxjUUpZQmdBQUFIUjFjbWx1WjNFRFdBTUFBQUJoWjJWeEJFc1hkVXNDZlhFRktHZ0NXQVlBQUFCdmRYbGhibWR4Qm1nRVN4cDFkUzQ9cQAu='
    dixc = peronal_data.encode()
    print(dixc)
    peronal_data = base64.b64decode((dixc))
    print(peronal_data)
    personal_dict = pickle.loads(peronal_data)
    print(personal_dict)


if __name__ == '__main__':
    # object_convert_into_string()
    # string_convert_into_object()
    # object_convert_string_by_base64()
    jiexi()
