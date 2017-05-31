# coding=utf-8
from flask_restful import Resource, marshal_with, reqparse
from sqlalchemy import or_

import config
import models
from app import db
from common import util
from common.reqparser_element import DateTime


class RepairResource(Resource):
    """报修资源"""
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('userId', type=int, required=True)
        self.parser.add_argument('houseId', type=int, required=True)

    @marshal_with(config.RESPONSE_FIELD)
    def post(self):
        """用户报修"""
        post_parser = self.parser.copy()
        post_parser.add_argument('communityId', type=int, required=True)
        post_parser.add_argument('userId', type=int, required=True)
        post_parser.add_argument('type', type=int, required=True)
        post_parser.add_argument('reporterTel', required=True)
        post_parser.add_argument('reporter', required=True)
        post_parser.add_argument('reportTime', type=DateTime, required=True)
        post_parser.add_argument('expectHandleTime', type=DateTime, required=True)
        post_parser.add_argument('reporterTel', required=True)
        post_parser.add_argument('description', required=True)
        args = post_parser.parse_args()
        args['status'] = config.REPAIR_REQUIRED
        repair = models.Repair()
        for key, value in args.iteritems():
            setattr(repair, key, value)
        db.session.add(repair)

    @marshal_with(config.RESPONSE_FIELD)
    def get(self, community_id, page_size, page):
        """分页查询报修情况"""
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=int, location='args')
        parser.add_argument('userId', type=int, location='args')
        parser.add_argument('status', type=int, location='args')
        parser.add_argument('keyword', location='args')
        args = parser.parse_args()
        type_value = args['type'] if args['type'] is not None else ''
        condition_type = '%%%s%%' % type_value
        status = args['status'] if args['status'] is not None else ''
        condition_status = '%%%s%%' % status
        keyword = args['keyword'] if args['keyword'] is not None else ''
        condition = '%%%s%%' % keyword
        user_id = args['userId']
        if user_id is None:
            fixes = models.Repair.query\
                .filter(or_(models.Repair.description.like(condition),
                            models.Repair.reporter.like(condition)))\
                .filter(models.Repair.type.like(condition_type))\
                .filter(models.Repair.status.like(condition_status))\
                .filter_by(communityId=community_id)\
                .order_by(models.Repair.reportTime.desc())\
                .paginate(page, page_size, error_out=False).items
        else:
            fixes = models.Repair.query \
                .filter(or_(models.Repair.description.like(condition),
                            models.Repair.reporter.like(condition))) \
                .filter(models.Repair.type.like(condition_type)) \
                .filter(models.Repair.status.like(condition_status)) \
                .filter_by(communityId=community_id) \
                .filter_by(userId=user_id) \
                .order_by(models.Repair.reportTime.desc()) \
                .paginate(page, page_size, error_out=False).items
        return {'data': util.serialize(fixes)}

    @marshal_with(config.RESPONSE_FIELD)
    def put(self, repair_id, status):
        """更改报修状态"""
        repair = models.Repair.query.filter_by(id=repair_id).first()
        if repair is None:
            return config.RESOURCE_NOT_EXISTS
        else:
            repair.status = status
            # db.session.commit()
