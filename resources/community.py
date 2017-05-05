from flask_restful import Resource, marshal_with, reqparse

import config
import models
from common import util


class CommunityCodeValidateResource(Resource):

    @marshal_with(config.RESPONSE_FIELD)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('communityId', type=int, required=True, location='args')
        parser.add_argument('code', required=True, location='args')
        args = parser.parse_args()
        community_id = args['communityId']
        code = args['code']
        result = models.Community.query\
            .filter_by(id=community_id, code=code).first()
        if result is None:
            return config.COMMUNITY_VALIDATE_ERROR


class CommunityCooperateValidateResource(Resource):
    @marshal_with(config.RESPONSE_FIELD)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('thirdPartyId', required=True, location='args')
        args = parser.parse_args()
        third_party_id = args['thirdPartyId']
        result = models.Community.query\
            .filter_by(thirdPartyId=third_party_id).first()
        if result is None:
            return config.COMMUNITY_NOT_COOPERATE
        else:
            return {'data': util.serialize(result)}
