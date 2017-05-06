# coding=utf-8
import datetime

import logging
from flask_restful import Resource, marshal_with, reqparse
from sqlalchemy import or_, and_

import config
import models
from app import db
from common import util
from common.reqparser_element import DateTime

logger = logging.getLogger(__name__)


class BoardMessageResource(Resource):

    @marshal_with(config.RESPONSE_FIELD)
    def post(self):
        """发送公告栏信息"""
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int)
        parser.add_argument('content', required=True)
        parser.add_argument('isTop', type=int)
        parser.add_argument('topStartTime', type=DateTime)
        parser.add_argument('topEndTime', type=DateTime)
        parser.add_argument('postTime', required=True, type=DateTime)
        parser.add_argument('source')
        args = parser.parse_args()

        user_id = args['userId']
        user = models.User.query.filter_by(id=user_id).first()

        if user_id is None:
            return config.USER_NOT_EXISTS
        # 如果有置顶，则判断用户权限
        is_top = args['isTop']
        if is_top is not None and is_top == 1:
            if user.roleId != config.ROLE_PROPERTY:
                return config.INSUFFICIENT_PRIVILEGE

        message = models.BoardMessage()
        message.communityId = user.communityId
        try:
            for key, value in args.iteritems():
                setattr(message, key, value)
            db.session.add(message)
            db.session.commit()
        except:
            db.session.rollback()
            return config.COMMON_ERROR

    @marshal_with(config.RESPONSE_FIELD)
    def get(self, community_id, page_size, page):
        """获取公告栏分页信息"""
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', location='args')
        parser.add_argument('userId', type=int, location='args')
        args = parser.parse_args()
        base_condition = '%%%s%%'
        keyword = args['keyword'] if args['keyword'] is not None else ''
        condition = base_condition % keyword
        user_id = args['userId']
        if user_id is not None and user_id != '':
            messages = models.BoardMessage.query\
                .filter_by(userId=user_id)\
                .filter(or_(models.BoardMessage.content.like(condition),
                            models.BoardMessage.source.like(condition)))\
                .filter(or_(models.BoardMessage.isTop.isnot(True),
                            and_(models.BoardMessage.topEndTime > datetime.datetime.now(),
                                 models.BoardMessage.topStartTime < datetime.datetime.now())))\
                .filter_by(communityId=community_id)\
                .order_by(models.BoardMessage.topStartTime.desc(),
                          models.BoardMessage.postTime.desc())\
                .paginate(page, page_size, error_out=False).items
        else:
            messages = models.BoardMessage.query \
                .filter(or_(models.BoardMessage.content.like(condition),
                            models.BoardMessage.source.like(condition),)) \
                .filter(or_(models.BoardMessage.isTop.isnot(True),
                            and_(
                                models.BoardMessage.topEndTime > datetime.datetime.now(),
                                models.BoardMessage.topStartTime < datetime.datetime.now()))) \
                .filter_by(communityId=community_id) \
                .order_by(models.BoardMessage.topStartTime.desc(),
                          models.BoardMessage.postTime.desc()) \
                .paginate(page, page_size, error_out=False).items

        return {'data': util.serialize(messages, ['password'])}
