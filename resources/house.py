from flask_restful import Resource, marshal_with, reqparse
from sqlalchemy import distinct

import config
import models
from app import db
from common import util


class HouseResource(Resource):
    @marshal_with(config.RESPONSE_FIELD)
    def get(self, community_id):
        # buildings = models.House.query\
        #     .filter_by(communityId=community_id).distinct().all()
        #
        building_select = 'SELECT DISTINCT building_id FROM house WHERE community_id=%d' % community_id
        connection = db.session.connection()
        buildings = connection.execute(building_select).fetchall()

        result = {
            'buildings': [],
            'units': [],
            'rooms': []
        }
        for building in buildings:
            building_value, = building
            result['buildings'].append(building_value)
            units_select = 'SELECT DISTINCT unit_id FROM house ' \
                           'WHERE community_id=%d AND building_id="%s"' \
                           % (community_id, building_value)
            units = connection.execute(units_select).fetchall()
            units_tmp = []
            units_rooms = []
            for unit in units:
                unit_value, = unit
                units_tmp.append(unit_value)
                rooms_select = 'SELECT DISTINCT room_id FROM house ' \
                               'WHERE community_id=%d AND building_id="%s"' \
                               ' AND unit_id="%s"' \
                               % (community_id, building_value, unit_value)
                rooms = connection.execute(rooms_select)
                rooms_tmp = []
                for room in rooms:
                    room_value, = room
                    rooms_tmp.append(room_value)
                units_rooms.append(rooms_tmp)
            result['rooms'].append(units_rooms)
            result['units'].append(units_tmp)

        return {'data': result}


class HouseIdResource(Resource):
    @marshal_with(config.RESPONSE_FIELD)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('communityId', type=int, location='args', required=True)
        parser.add_argument('buildingId', location='args', required=True)
        parser.add_argument('unitId', location='args', required=True)
        parser.add_argument('roomId', location='args', required=True)
        args = parser.parse_args()
        community_id = args['communityId']
        building_id = args['buildingId']
        unit_id = args['unitId']
        room_id = args['roomId']
        house = models.House.query.filter_by(communityId=community_id,
                                             buildingId=building_id,
                                             unitId=unit_id,
                                             roomId=room_id).first()
        return {'data': util.serialize(house)}
