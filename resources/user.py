# coding=utf-8
"""
在密码加密这一方面，暂时规定所有的加密都放在前端，而后台只负责简单的进行比对
"""
import time
from flask_restful import Resource, marshal_with, reqparse

import config
import models
from app import db
from common import util
from common.reqparser_element import DateTime


class UserResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', required=True)
        self.parser.add_argument('password', required=True)
        self.parser.add_argument('roleId', type=int, required=True)
        self.parser.add_argument('avatar')
        self.parser.add_argument('background')
        self.parser.add_argument('nickname')
        self.parser.add_argument('tel')
        self.parser.add_argument('gender')
        self.parser.add_argument('communityId', type=int, required=True)
        self.parser.add_argument('houseId', type=int)
        self.parser.add_argument('birthday', type=DateTime)

    @marshal_with(config.RESPONSE_FIELD)
    def post(self):
        """用户注册"""

        user = self.parser.parse_args()
        username = user['username']
        pre_user = models.User.query.filter_by(username=username).first()
        if pre_user is not None:
            return config.USERNAME_CONFLICT
        user_model = models.User()
        for key, value in user.iteritems():
            setattr(user_model, key, value)
        db.session.add(user_model)

    @marshal_with(config.RESPONSE_FIELD)
    def get(self, user_id):
        """获取某个用户信息"""

        user = models.User.query.filter_by(id=user_id).first()
        return {'data': util.serialize(user)}

    @marshal_with(config.RESPONSE_FIELD)
    def put(self, user_id):
        pre_user = models.User.query.filter_by(id=user_id).first()
        if pre_user is None:
            return config.RESOURCE_NOT_EXISTS
        else:
            parser = self.parser
            parser.replace_argument('password', required=False)
            parser.replace_argument('username', required=False)
            parser.replace_argument('roleId', type=int, required=False)
            parser.replace_argument('communityId', type=int, required=False)
            user = parser.parse_args()
            for key, value in user.iteritems():
                if value is not None:
                    if isinstance(value, int) and value == 0:
                        continue
                    else:
                        setattr(pre_user, key, value)


class LoginResource(Resource):

    @marshal_with(config.RESPONSE_FIELD)
    def post(self):
        """用户登录"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        user = parser.parse_args()
        result = models.User.query.filter_by(username=user['username'],
                                             password=user['password']).first()
        if result is not None:
            return {'data': util.serialize(result, ['password'])}
        else:
            return config.USERNAME_OR_PASSWORD_ERROR


class PasswordResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=int, required=True)
        self.parser.add_argument('password', required=True)

    @marshal_with(config.RESPONSE_FIELD)
    def put(self):
        """
        更改密码，在前端需要先验证原密码的正确性，再调用此接口
        """
        args = self.parser.parse_args()
        user_id = args['id']
        password = args['password']
        user = models.User.query.filter_by(id=user_id).first()
        if user is None:
            return config.RESOURCE_NOT_EXISTS
        else:
            user.password = password


class UserHouseResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('userId', type=int, required=True)
        self.parser.add_argument('houseId', type=int, required=True)

    def put(self):
        """更改用户地址"""
        args = self.parser.parse_args()
        user_id = args['userId']
        house_id = args['houseId']
        user = models.User.query.filter_by(id=user_id).first()
        if user is None:
            return config.RESOURCE_NOT_EXISTS
        else:
            if user.roleId == config.ROLE_PROPERTY:
                return config.PROPERTY_NOT_ALLOW_CHANGE_HOUSE
            else:
                user.houseId = house_id
