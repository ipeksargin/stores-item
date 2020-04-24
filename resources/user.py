import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

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