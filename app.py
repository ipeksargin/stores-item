import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from auth import authenticate, identity
from resources.user import UserRegister, UserMethod
from resources.item import Item, ItemList
from db import db
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "mynewsecretkeyy"
api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app,authenticate,identity) #/auth


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserMethod, '/user/<int:user_id>')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')


if __name__=='__main__':
    app.run(port=4998, debug=True)
