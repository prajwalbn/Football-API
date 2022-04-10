import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.manager import ManagerRegister
from resources.player import Player, PlayerList
from resources.club import Club, ClubList

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL1', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'group4cloudproject'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Club, '/club/<string:name>')
api.add_resource(Player, '/player/<string:name>')
api.add_resource(PlayerList, '/players')
api.add_resource(ClubList, '/clubs')

api.add_resource(ManagerRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)