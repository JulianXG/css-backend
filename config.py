# coding=utf-8
from flask_restful import fields

# DB_URL = 'mysql://root:root@mysql:3306/css?charset=utf8'
DB_URL = 'mysql://root:ease1234@mysql:3306/css?charset=utf8'

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
ROLE_PROPERTY = 1
ROLE_OWNER = 2

# 支付状态
PAY_REQUIRED = 0
PAY_FINISHED = 1

# 报修类型
REPAIR_TYPE_HOUSE = 1
REPAIR_TYPE_ELECTRICITY = 2
REPAIR_TYPE_FACILITY = 3

# 报修状态
REPAIR_REQUIRED = 0
REPAIR_REPAIRING = 1
REPAIR_FINISH = 2

REPAIR_PUBLISH_REQUIRED = 0
REPAIR_PUBLISH_FINISHED = 1

RESPONSE_FIELD = {
    'code': fields.Integer(default=200),
    'message': fields.String(default=u'请求成功'),
    'data': fields.Raw
}

USERNAME_OR_PASSWORD_ERROR = {
    'code': 400,
    'message': u'用户名或密码错误'
}

USERNAME_CONFLICT = {
    'code': 401,
    'message': '注册用户名冲突'
}

USER_NOT_EXISTS = {
    'code': 402,
    'message': '用户不存在'
}

# 用户登录相关
RESOURCE_NOT_EXISTS = {
    'code': 404,
    'message': '所请求的资源不存在'
}

# 物业权限相关
REQUIRE_COMMUNITY_CODE = {
    'code': 430,
    'message': '物业注册需要提供正确的社区码'
}

PROPERTY_NOT_ALLOW_CHANGE_HOUSE = {
    'code': 431,
    'message': '物业账号不允许切换地址'
}

# 权限相关
INSUFFICIENT_PRIVILEGE = {
    'code': 420,
    'message': '操作失败，用户权限不够'
}

COMMUNITY_VALIDATE_ERROR = {
    'code': 421,
    'message': '社区码验证失败'
}

COMMUNITY_NOT_COOPERATE = {
    'code': 422,
    'message': '该社区目前没有与我们合作'
}

COMMON_ERROR = {
    'code': 480,
    'message': '请求失败，请检查请求，并尝试重试'
}
