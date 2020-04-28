import sqlite3
from flask_restful import Resource,request
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,create_refresh_token,
jwt_refresh_token_required,get_jwt_identity,jwt_required,get_raw_jwt)
from blacklist import BLACKLIST
from schemas.user import UserSchema
from marshmallow import ValidationError

user_schema = UserSchema()
class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            get_json = request.get_json()
            user = user_schema.load(get_json)
        except ValidationError as err:
                return err.messages, 400

        if UserModel.find_by_username(user.username):
            return {'message':'This username already exists'},404

        user.save_to_db()
        return {'message':'User created'}, 201


class UserMethod(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'},404
        return user_schema.dump(user),200

    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'}
        user.delete_from_db()
        return {'message':'User deleted'}

class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            get_json = request.get_json()
            data = user_schema.load(get_json) #request parse
        except ValidationError as err:
            return err.messages,400
        user = UserModel.find_by_username(data.username)

        if user and safe_str_cmp(user.password, data.password):
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    'access-token': access_token,
                    'refresh-token': refresh_token
                },200
            return {'message':'User should be activated'},400
        return {'message':'Invalid credentails'},401

class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt['jti'] #jti is uniques identifier for jwt.
        BLACKLIST.add(jti)
        return {'message': 'Logged out'},200
class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user,fresh=False) #gives you new access token
        return {'message':new_access_token},200
