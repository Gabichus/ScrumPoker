from app import app, api, db, socketio, jwt
from flask_restful import Api, Resource, reqparse
from app.models import User as userModel


class User(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gmail', type=str)

        gmail = parser.parse_args()['gmail']

        user = userModel(gmail=gmail)
        db.session.add(user)
        db.session.commit()
        users = [ {'id':u.id,'gmail':u.gmail} for u in userModel.query.all() ]
        return users

    def get(self):
        users = [ {'id':u.id,'gmail':u.gmail} for u in userModel.query.all() ]
        return users
