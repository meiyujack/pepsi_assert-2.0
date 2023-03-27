from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


class WebSecurity:

    def __init__(self, secret_key):
        self.serializer = URLSafeTimedSerializer(secret_key)

    def generate_token(self, info: dict):
        token = self.serializer.dumps(info)
        return token

    def get_info_by_token(self, token, key, max_age=3 * 24 * 60 * 60):
        """
        获取加密内容
        :param token: 待解析内容
        :param key: 待解析内容的key
        :param max_age: 保持时间。单位s
        :return: Any|None
        """
        try:
            info = self.serializer.loads(token, max_age=max_age)
        except BadSignature or SignatureExpired:
            return None
        return info[key]

    def check_token(self, token):
        try:
            self.serializer.loads(token)
        except BadSignature or SignatureExpired:
            return False
        return True
