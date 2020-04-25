import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,create_refresh_token


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    help="This field cannot be empty.",
    required =True
    )
    parser.add_argument('password',
    type=str,
    help="This field cannot be empty.",
    required =True
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'This username already exists'},404

        user = UserModel(**data)
        user.save_to_db()

        return {'message':'User created'}, 201


class UserMethod(Resource):
    @classmethod
    def get_user(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'},404
        return user.json()

    @classmethod
    def delete_user(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'}
        user.delete_from_db()
        return {'message':'User deleted'}

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    help="This field cannot be empty.",
    required =True
    )
    parser.add_argument('password',
    type=str,
    help="This field cannot be empty.",
    required =True
    )
    
    @classmethod
    def post(cls):
        data = cls.parser.parse_args() #request parse
        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access-token': access_token,
                'refresh-token': refresh_token
            },200
        return {'message':'Invalid credentails'},401

        