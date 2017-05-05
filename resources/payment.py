# coding=utf-8
import datetime
from flask_restful import Resource, marshal_with, reqparse

import config
import models
from app import db
from common import util
from common.reqparser_element import DateTime


class PropertyFee(Resource):
    @marshal_with(config.RESPONSE_FIELD)
    def post(self):
        """
        物业为业主提交某年的物业费接口
        :return: 接口请求结果
        """
        parser = reqparse.RequestParser()
        parser.add_argument('communityId', type=int, required=True)
        parser.add_argument('year', type=int, required=True)
        parser.add_argument('deadline', type=DateTime, required=True)
        args = parser.parse_args()
        community_id = args['communityId']
        year = args['year']
        deadline = args['deadline']
        pre_count = models.PropertyFee.query\
            .filter_by(communityId=community_id)\
            .count()
        if pre_count == 0:
            try:
                houses = models.House.query.filter_by(communityId=community_id).all()
                for house in houses:
                    fee = models.PropertyFee()
                    fee.communityId = community_id
                    fee.houseId = house.id
                    fee.status = config.PAY_REQUIRED
                    fee.year = year
                    fee.deadline = deadline
                    fee.amount = house.propertyFee
                    db.session.add(fee)
                db.session.commit()
            except:
                db.session.rollback()
                return config.COMMON_ERROR

    @marshal_with(config.RESPONSE_FIELD)
    def get(self, community_id, page_size, page):
        """查询小区的物业费缴费情况"""
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=int, location='args')
        parser.add_argument('year', type=int, location='args')
        parser.add_argument('houseId', type=int, location='args')
        args = parser.parse_args()
        base_condition = '%%%s%%'
        status = args['status'] if args['status'] is not None else ''
        condition_status = base_condition % status
        house_id = args['houseId']
        if house_id is None:
            fees = models.PropertyFee.query\
                .filter_by(communityId=community_id)\
                .filter(models.PropertyFee.status.like(condition_status))\
                .order_by(models.PropertyFee.id.desc())\
                .paginate(page, page_size, error_out=False).items
        else:
            fees = models.PropertyFee.query \
                .filter_by(communityId=community_id) \
                .filter_by(houseId=house_id) \
                .filter(models.PropertyFee.status.like(condition_status)) \
                .order_by(models.PropertyFee.id.desc()) \
                .paginate(page, page_size, error_out=False).items
        return {'data': util.serialize(fees)}


class PropertyFeeStatus(Resource):

    @marshal_with(config.RESPONSE_FIELD)
    def get(self, community_id, year):
        """获取社区某一年物业费发布状态"""
        year_format = datetime.datetime.strptime(year, "%Y")
        result = models.PropertyFee.query\
            .filter_by(communityId=community_id, year=year_format)\
            .first()
        if result is None:
            return config.RESOURCE_NOT_EXISTS
