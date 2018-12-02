from Billboard import DataBase as db

from flask_login import UserMixin
from werkzeug import generate_password_hash, check_password_hash

from Billboard import MarshMallow as ma
from flask_marshmallow import Marshmallow


class User_Model (db.Model, UserMixin):

    __tablename__ = 'user_model'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique=True , nullable = False)
    pass_hash = db.Column(db.String(54))
    credit = db.Column (db.Integer)
    role = db.Column (db.String (10) , nullable = False)


    def __init__ (self , name , email , password, role):

        if role in ['user', 'admin']:
            self.name = name
            self.email = email.lower()
            self.pass_hash = generate_password_hash (password)
            self.credit = 2000
            self.role = role

        else:
            raise ValueError()


    def add_and_commit (self):
        db.session.add (self)
        db.session.commit()


    def check_password (self,password):
        return check_password_hash (self.pass_hash,password)


    @staticmethod
    def email_query (req):
        return User_Model.query.filter_by (email = req).first()


    def discharge (self , cost):
        self.credit -= cost
        db.session.commit()

    def charge (self, cost):
        self.credit += cost
        db.session.commit()


    def serialize_one (self):
        return User_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return User_Model_Schema(many = True).dump (arg).data



class User_Model_Schema (ma.ModelSchema):
    class Meta:
        model = User_Model
        exclude = ('pass_hash',)