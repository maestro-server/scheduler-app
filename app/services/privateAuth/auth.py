import jwt
from instance.config import Config

class PrivateAuth(object):

    @staticmethod
    def create_token(info):
        body = {
            **info,
            'noauth': Config.NOAUTH
        }

        return PrivateAuth.encode(body)

    @staticmethod
    def encode(body):
        return jwt.encode(body, Config.SECRETJWT_PRIVATE, algorithm='HS256').decode('utf-8')

    @staticmethod
    def decode(encoded):
        return jwt.decode(encoded, Config.SECRETJWT_PRIVATE, algorithms=['HS256'])
