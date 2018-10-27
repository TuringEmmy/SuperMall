# author    python
# time      18-10-27 下午4:15
# project   SuperMall

def jwt_response_payload_handler(token, user=None, request=None):
    """自定义jwt认证成功返回的数据"""

    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }
