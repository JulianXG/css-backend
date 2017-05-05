from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(40))
    avatar = db.Column(db.String)
    background = db.Column(db.String)
    nickname = db.Column(db.String(20))
    birthday = db.Column(db.Date)
    roleId = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
    gender = db.Column(db.String(4))
    communityId = db.Column('community_id', db.Integer, db.ForeignKey('community.id'))
    houseId = db.Column('house_id', db.Integer, db.ForeignKey('house.id'))
    tel = db.Column(db.String)
    role = db.relationship('Role', uselist=False, lazy='joined')
    community = db.relationship('Community', uselist=False, lazy='joined')
    house = db.relationship('House', uselist=False, lazy='joined')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)


class BoardMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    communityId = db.Column('community_id', db.Integer, db.ForeignKey('community.id'))
    isTop = db.Column('is_top', db.Boolean)
    content = db.Column(db.String)
    topStartTime = db.Column('top_start_time', db.DateTime)
    topEndTime = db.Column('top_end_time', db.DateTime)
    source = db.Column(db.String(20))
    postTime = db.Column('post_time', db.DateTime)
    user = db.relationship('User', uselist=False, lazy='joined')


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    propertyId = db.Column('property_id', db.Integer, db.ForeignKey('property.id'))
    name = db.Column(db.String(20))
    address = db.Column(db.String(40))
    code = db.Column(db.String)
    cooperationTime = db.Column('cooperation_time', db.DateTime)
    thirdPartyId = db.Column('third_party_id', db.String)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    tel = db.Column(db.String(13))


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ownerName = db.Column('owner_name', db.String(20))
    communityId = db.Column('community_id', db.Integer, db.ForeignKey('community.id'))
    buildingId = db.Column('building_id', db.String)
    unitId = db.Column('unit_id', db.String)
    roomId = db.Column('room_id', db.String)
    propertyFee = db.Column('property_fee', db.Float)
    area = db.Column(db.Float)


class PropertyFee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    communityId = db.Column('community_id', db.Integer, db.ForeignKey('community.id'))
    houseId = db.Column('house_id', db.Integer, db.ForeignKey('house.id'))
    status = db.Column(db.Integer)
    year = db.Column(db.Date)
    amount = db.Column(db.Float)
    deadline = db.Column(db.DateTime)
    payTime = db.Column('pay_time', db.DateTime)
    house = db.relationship('House', uselist=False, lazy='joined')


class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    communityId = db.Column('community_id', db.Integer, db.ForeignKey('community.id'))
    houseId = db.Column('house_id', db.Integer, db.ForeignKey('house.id'))
    type = db.Column(db.Integer)
    reportTime = db.Column('post_time', db.DateTime)
    reporter = db.Column(db.String)
    reporterTel = db.Column('reporter_tel', db.String)
    expectHandleTime = db.Column('expect_handle_time', db.DateTime)
    description = db.Column(db.String)
    status = db.Column(db.Integer)
