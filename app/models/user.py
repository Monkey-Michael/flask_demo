from flask import  current_app
from flask_login import AnonymousUserMixin ,UserMixin
from  itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature,SignatureExpired
from werkzeug.security import  check_password_hash,generate_password_hash

from .. import db,login_manager

class Permission:
    GENERAL = 0x01
    ADMINISTER = 0Xff


class Role(db.Model):
    __table__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean,default=False,index=True)
    Permission = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.GENERAL, 'main', True),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                #todo