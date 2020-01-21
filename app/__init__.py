from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
socketio = SocketIO(app, cors_allowed_origins='*')
api = Api(app)
CORS(app)
jwt = JWTManager(app)
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_HEADER_TYPE'] = ""



from app import routes, models, services