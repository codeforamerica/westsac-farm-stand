from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db, login_manager, ma



class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    ADD_PRODUCT = 0x04
    ADD_MARKET = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT, True),
            'Farmer': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.ADD_PRODUCT |
                          Permission.ADD_MARKET, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class Interestedpeople(db.Model):
    __tablename__ = 'interestedpeople'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    phone = db.Column(db.String(64))

    def __repr__(self):
        return '<Name %r>' % self.name

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    status = db.Column(db.String(32))
    price = db.Column(db.String(12))
    starts = db.Column(db.String(64))
    ends = db.Column(db.String(64))
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Product %r>' % (self.name)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    phone = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    url = db.Column(db.String(128), unique=True, index=True)
    farm_name = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    about_me = db.Column(db.Text())
    location = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    products = db.relationship('Product', backref='farmer', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FARMSTAND_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        
        return True

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('user')
        if id:
            return User.query.get(id)
        return None

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserSchema(ma.ModelSchema):
    class Meta:
        # Fields to expose
        model = User
        fields = ('id','email', 'phone', 'location', 'phone', 'url', 'farm_name', 'name', 'about_me', 'member_since', 'last_seen', 'products')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
