from app import app, api, db, socketio, jwt
from flask_restful import Api, Resource, reqparse
from app.models import Task as taskModel, Project as projectModel, TaskVoting as taskVotingModel
from app.services import TaskSchema
from flask_socketio import send, emit, Namespace
from sqlalchemy import asc
from app.services import deleteTaskRecursion, getProjectTasks
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from app.common.jwt_decorator import jwt_decorator

class Project(Resource):
    @jwt_required
    def get(self, id):
        # request.args['param']
        project = projectModel.query.get(id)
        if not project:
            return None

        project = getProjectTasks(project.id)
        return project

    @jwt_decorator()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('flag', type=bool)

        name = parser.parse_args()['name']
        description = parser.parse_args()['description']
        flag = parser.parse_args()['flag']

        project = projectModel(name=name, description=description, flag=flag)
        db.session.add(project)
        db.session.commit()

        socketData = getProjectTasks(project.id)
        socketio.emit('project', data=socketData, namespace='/poker')

        return socketData
    
    @jwt_decorator()
    def put(self, id):
        project = projectModel.query.get(id)
        if not project:
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)

        name = parser.parse_args()['name']
        description = parser.parse_args()['description']

        if description:
            project.description = description
        project.name = name

        db.session.commit()
        
        project = getProjectTasks(id)

        socketio.emit('project', data=project, namespace='/poker')

        return project
    
    @jwt_decorator()
    def delete(self, id):
        pr = projectModel.query.get(id)
        if not pr:
            return None
        pr.member=[]
        db.session.commit()
        for t in pr.tasks:
            t_sh = TaskSchema()
            result = t_sh.dump(t)
            deleteTaskRecursion(result)
            taskVotingModel.query.filter_by(task_id=t.id).delete()
            db.session.delete(t)
        db.session.delete(pr)
        db.session.commit()

class ProjectList(Resource):
    @jwt_required
    # @jwt_decorator()
    def get(self):
        projects = projectModel.query.order_by(asc(projectModel.id)).all()
        if not projects:
            return None
        allProject = []
        for project in projects:
            project = getProjectTasks(project.id)
            allProject.append(project)
        return allProject
