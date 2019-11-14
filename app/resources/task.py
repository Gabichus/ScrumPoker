from app import app, api, db, socketio, jwt
from flask_restful import Api, Resource, reqparse
from app.models import Task as taskModel, Project as projectModel
from app.services import TaskSchema, getProjectTasks
from flask_socketio import send, emit, Namespace
from sqlalchemy import asc

class Task(Resource):
    def get(self, id):
        sh = TaskSchema()

        return sh.dump(taskModel.query.get(id))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('parent_id', type=int)
        parser.add_argument('description', type=str)
        parser.add_argument('project_id', type=int)
        parser.add_argument('flag', type=bool)

        name = parser.parse_args()['name']
        parent_id = parser.parse_args()['parent_id']
        description = parser.parse_args()['description']
        project_id = parser.parse_args()['project_id']
        flag = parser.parse_args()['flag']

        if projectModel.query.get(project_id) is None:
            return None

        task = taskModel(name=name, description=description,
                         project_id=project_id, flag=flag)
        db.session.add(task)
        db.session.commit()

        if parent_id is not None:
            parent = taskModel.query.get(parent_id)
            parent.child_task.append(task)
            db.session.commit()

        socketData = getProjectTasks(project_id)
        socketio.emit('project', data=socketData, namespace='/poker')
        sh = TaskSchema(many=False, only=(
            'id', 'name', 'description', 'voting_status', 'time', 'flag'))

        return sh.dump(task)

    def put(self, id):
        task = taskModel.query.get(id)
        if not task:
            return None

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)

        name = parser.parse_args()['name']
        description = parser.parse_args()['description']
        project_id = task.project_id

        if description:
            task.description = description
        task.name = name

        db.session.commit()

        socketData = getProjectTasks(project_id)
        socketio.emit('project', data=socketData, namespace='/poker')

    def delete(self, id):
        taskRemove = taskModel.query.get(id)
        if taskRemove is not None and taskRemove.child_task.first() is None:
            taskRemoveParent = taskRemove.parent.first()
            project_id = taskRemove.project_id
            if taskRemoveParent is not None:
                taskRemoveParent.child_task.remove(taskRemove)
            db.session.delete(taskRemove)
            db.session.commit()

        socketData = getProjectTasks(project_id)
        socketio.emit('project', data=socketData, namespace='/poker')
