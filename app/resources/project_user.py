from app import app, api, db, socketio, jwt
from flask_restful import Api, Resource, reqparse
from app.models import User as userModel, Project as projectModel
from sqlalchemy import asc
from app.common.jwt_decorator import jwt_decorator


class ProjectUser(Resource):
    @jwt_decorator()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('project_id', type=int)
        parser.add_argument('status', type=bool)

        user_id = parser.parse_args()['user_id']
        project_id = parser.parse_args()['project_id']
        status = parser.parse_args()['status']

        pr = projectModel.query.get(project_id)
        user = userModel.query.get(user_id)

        if pr and user:
            if status:
                pr.members.append(user)
                db.session.commit()
            else:
                pr.members.remove(user)
                db.session.commit()

        socketio.emit('client', data="", namespace='/client')

        return self.get(project_id)

    @jwt_decorator()
    def get(self,id):
        pr = projectModel.query.get(id)
        if pr:
            mem = [{'id':user.id, 'gmail':user.gmail, 'status': True} for user in pr.members]
            users = {x for x in userModel.query.all()} - {x for x in pr.members}
            [mem.append({'id':user.id, 'gmail':user.gmail, 'status': False}) for user in users]
            return mem
        return None

        

        