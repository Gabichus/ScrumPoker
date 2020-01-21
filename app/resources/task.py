from app import app, api, db, socketio, jwt
from flask_restful import Api, Resource, reqparse
from app.models import Task as taskModel, Project as projectModel, TaskVoting as taskVotingModel
from app.services import TaskSchema, getProjectTasks, projectTimeCalc
from flask_socketio import send, emit, Namespace
from sqlalchemy import asc, and_
from flask_jwt_extended import jwt_required
from app.common.jwt_decorator import jwt_decorator


class Task(Resource):
    @jwt_required
    def get(self, id):
        sh = TaskSchema()
        return sh.dump(taskModel.query.get(id))
    
    @jwt_decorator()
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
        socketio.emit('client', data="", namespace='/client')

        sh = TaskSchema(many=False, only=(
            'id', 'name', 'description', 'voting_status', 'time', 'flag'))

        return sh.dump(task)
    
    @jwt_decorator()
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
        socketio.emit('client', data="", namespace='/client')
   
    @jwt_decorator()
    def delete(self, id):
        taskRemove = taskModel.query.get(id)
        if taskRemove is not None and taskRemove.child_task.first() is None:
            taskRemoveParent = taskRemove.parent.first()
            project_id = taskRemove.project_id  # for create dump for socket
            if taskRemoveParent is not None:
                taskRemoveParent.child_task.remove(taskRemove)
            taskVotingModel.query.filter_by(task_id=id).delete()
            db.session.delete(taskRemove)
            db.session.commit()

        socketData = getProjectTasks(project_id)
        socketio.emit('project', data=socketData, namespace='/poker')
        socketio.emit('client', data="", namespace='/client')
   
    @jwt_decorator()
    def patch(self, id):
        task = taskModel.query.get(id)
        pr = task.project
        taskVotingTrue = pr.tasks.filter(and_(taskModel.voting_status == True, taskModel.child_task == None)).all()

        sh = TaskSchema(many=False, only=(
            'id', 'name', 'description', 'voting_status', 'time', 'flag'))

        parser = reqparse.RequestParser()
        parser.add_argument('voting_status', type=bool)
        parser.add_argument('time', type=int)

        voting_status = parser.parse_args()['voting_status']
        time = parser.parse_args()['time']
        
        print(time, voting_status)

        if taskVotingTrue and voting_status:
            return sh.dump(task)

        if time is not None:
            task.time = time
        task.voting_status = voting_status
        db.session.commit()

        if not voting_status or time:
            projectTimeCalc(pr.id)

        socketio.emit('client', data="", namespace='/client')

        return sh.dump(task)
