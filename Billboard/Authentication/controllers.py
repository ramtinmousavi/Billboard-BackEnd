from flask import request, jsonify, session, Blueprint
from flask_login import login_required, login_user, logout_user

from Billboard.Authentication.models import User_Model


authentication = Blueprint('authentication', __name__)



class Authentication:

    @staticmethod
    def sign_up():

        if request.method == 'POST':

            req = request.get_json()

            name = req["name"]
            email = req["email"]
            password = req["password"]

            new_user = User_Model(name, email, password,'user')
            new_user.add_and_commit()

            out = {'user':new_user.serialize_one() , 'status':'OK'}
            return jsonify(out)

        out = {'user':'', 'status':'method is not POST'}
        return jsonify (out)



    @staticmethod
    def login():

        if request.method == 'POST' :

            req = request.get_json()

            email = req["email"]
            password = req["password"]

            stored_user = User_Model.email_query (email)

            if (stored_user is not None) and (stored_user.check_password(password)):

                login_user (stored_user)
                session ['user_id'] = stored_user.id
                session ['role'] = stored_user.role

                out = {'user':stored_user.serialize_one(), 'status':'OK'}

                return jsonify (out)


            else:
                if stored_user is None:
                    out = {'user':'', 'status':'user not found'}
                    return jsonify (out)

                elif not stored_user.check_password(req['password']):
                    out = {'user':'' , 'status':'password incorrect'}
                    return jsonify (out)

        else:
            out = {'user':'', 'status':'method is not POST'}
            return jsonify (out)


    @staticmethod
    @login_required
    def logout ():

        user_id = session.pop ('user_id', None)
        session.pop ('role', None)

        logout_user()

        user = User_Model.query.get (user_id)

        out = {'user': user.serialize_one(), 'status':'OK'}
        return jsonify (out)



authentication.add_url_rule('/api/signup' , view_func = Authentication.sign_up , methods = ['POST' , 'GET'])
authentication.add_url_rule('/api/login' , view_func = Authentication.login , methods = ['POST' , 'GET'])
authentication.add_url_rule('/api/logout' , view_func = Authentication.logout)