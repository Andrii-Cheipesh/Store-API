import os
import re

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resourses.user import UserRegister
from resourses.item import Item, ItemAll
from resourses.store import Store, StoresAll

uri = os.getenv('DATABASE_URL')
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "invcloak"
api = Api(app)


# initiate a JWT object, that going to use app, authenticate and identity func TOGETHER
jwt = JWT(app, authenticate, identity)  # create new endpoint: /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoresAll, "/stores")
api.add_resource(ItemAll, "/items")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
