import logging
import sys

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

reload(sys)
sys.setdefaultencoding("utf-8")
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='[%(asctime)s] [%(levelname)s] %(filename)s(%(funcName)s:%(lineno)d): %(message)s',
                    stringeam=sys.stdout)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql:3306/css?charset=utf8'
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = True
db = SQLAlchemy(app, session_options={'autocommit': True})
CORS(app, supports_credentials=True)

import models
from resources.user import UserResource, PasswordResource, \
    UserHouseResource, LoginResource
from resources.board_message import BoardMessageResource
from resources.community import CommunityCodeValidateResource, \
    CommunityCooperateValidateResource
from resources.payment import PropertyFee, PropertyFeeStatus
from resources.repair import RepairResource
from resources.house import HouseResource, HouseIdResource

v1_blueprint = Blueprint('api', __name__)
api = Api(v1_blueprint)

api.add_resource(LoginResource, '/login')
api.add_resource(UserResource, '/register', '/users/<int:user_id>')
api.add_resource(BoardMessageResource, '/messages',
                 '/messages/<int:community_id>/<int:page_size>/<int:page>')
api.add_resource(CommunityCodeValidateResource, '/communities/code')
api.add_resource(PropertyFee, '/propertyFee',
                 '/propertyFee/<int:community_id>/<int:page_size>/<int:page>')
api.add_resource(PasswordResource, '/password')
api.add_resource(UserHouseResource, '/users/houses')
api.add_resource(RepairResource, '/fixes',
                 '/fixes/<int:repair_id>/<int:status>',
                 '/fixes/<int:community_id>/<int:page_size>/<int:page>')
api.add_resource(CommunityCooperateValidateResource, '/cooperate/communities')
api.add_resource(HouseResource, '/houses/<int:community_id>')
api.add_resource(HouseIdResource, '/houses')
api.add_resource(PropertyFeeStatus,
                 '/propertyFee/status/<int:community_id>/<year>')

app.register_blueprint(v1_blueprint, url_prefix='/v1')


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
