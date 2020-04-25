import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserMethod, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from db import db
from resources.store import Store, StoreList
from blacklist import BLACKLIST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = "mynewsecretkeyy"
api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) 

@jwt.token_in_blacklist_loader
def token_if_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST #this will call revoked token func

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity ==1:
        return {'is_admin':True}
    return {'is_admin':False}

@jwt.expired_token_loader
def expired_token_callback(): #the function will be called when token is expired
    return {'description':'The token has expired',
            'error':'token_expired'},401

@jwt.invalid_token_loader #when it is not a proper jwt
def invalid_token_callback(error):
    return {'description':'Not a JWT token',
            'error':'invalid_token'},401

@jwt.unauthorized_loader #when jwt hasnt been sent
def missing_token_callback(error):
    return {'description':'The token is missing',
            'error':'missing_token'},401

@jwt.needs_fresh_token_loader
def fresh_token_callback():
    return {'description':'The token needs to be freshed',
            'error':'need_fresh_token'},401

@jwt.revoked_token_loader
def revoked_token_callback():
    return {'description':'The user dont have access',
            'error':'token_revoked'},401



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')


if __name__=='__main__':
    app.run(port=4998, debug=True)
