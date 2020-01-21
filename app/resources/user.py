from app import app, api, db, socketio, jwt
from flask_restful import Api, Resource, reqparse
from app.models import User as userModel, TaskVoting as taskVotingModel
from app.common.jwt_decorator import jwt_decorator
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import asc


class User(Resource):
    @jwt_decorator()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gmail', type=str)

        gmail = parser.parse_args()['gmail']

        user = userModel(gmail=gmail)
        db.session.add(user)
        db.session.commit()
        users = [{'id': u.id, 'gmail': u.gmail, 'admin': u.admin} for u in userModel.query.filter(
            userModel.id != get_jwt_identity()).order_by(asc(userModel.id))]
        return users

    @jwt_decorator()
    def get(self):
        users = [{'id': u.id, 'gmail': u.gmail, 'admin': u.admin} for u in userModel.query.filter(
            userModel.id != get_jwt_identity()).order_by(asc(userModel.id))]
        return users

    @jwt_decorator()
    def delete(self, id):
        user = userModel.query.get(id)
        if user:
            user.projects = []
            taskVotingModel.query.filter_by(user_id=id).delete()
            db.session.delete(user)
            db.session.commit()
        return self.get()

    @jwt_decorator()
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('admin', type=bool)

        admin = parser.parse_args()['admin']

        print(id, admin)
        user = userModel().query.get(id)
        user.admin = admin

        db.session.commit()
        users = [{'id': u.id, 'gmail': u.gmail, 'admin': u.admin} for u in userModel.query.filter(
            userModel.id != get_jwt_identity()).order_by(asc(userModel.id))]
        return users
