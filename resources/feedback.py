# coding=utf-8
from flask_restful import Resource, reqparse, marshal_with

import config
import models
from app import db
from common.reqparser_element import DateTime


class FeedbackResource(Resource):

    @marshal_with(config.RESPONSE_FIELD)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=int, required=True)
        parser.add_argument('content', required=True)
        parser.add_argument('postTime', required=True, type=DateTime)
        data = parser.parse_args()
        feedback = models.Feedback()
        for key, value in data.iteritems():
            setattr(feedback, key, value)
        db.session.add(feedback)
