import jwt
from instance.config import Config
from flask import request
from app.services.privateAuth.error.privateUnauthorized import PrivateUnauthorizedError


class PrivateAuth(object):
    @staticmethod
    def autheticate():
        auth_token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            auth_token = auth_header.split(" ")[1]

        if auth_token:
            resp = PrivateAuth.decode(auth_token)

            if resp.get('noauth') == Config.NOAUTH:
                return resp

        raise PrivateUnauthorizedError('Unauthorized')

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
