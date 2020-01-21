from app import app, api, db, socketio, jwt
from flask_restful import Api, Resource, reqparse
from app.models import User as userModel, Project as projectModel, Task as taskModel, TaskVoting as taskVotingModel
from app.services import getProjectTasks, TaskSchema, taskCalcTime
from sqlalchemy import and_
from flask_jwt_extended import jwt_required, get_jwt_identity

class ProtectedUser(Resource):
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('reqType', type=str)

        reqType = parser.parse_args()['reqType']

        user = userModel.query.get(get_jwt_identity())

        if reqType == "projects":
            projects = [getProjectTasks(p.id) for p in user.projects]
            return projects
        elif reqType == "tasks":
            tasks = []
            sh = TaskSchema(many=False, only=(
                'id', 'name', 'description', 'voting_status', 'time', 'flag'))
            for p in user.projects:
                [tasks.append(sh.dump(t)) for t in p.tasks if t.voting_status is True]
            return tasks
        return None
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('time', type=int, nullable=False)
        parser.add_argument('task_id', type=int, nullable=False)

        time = parser.parse_args()['time']
        task_id = parser.parse_args()['task_id']

        task = taskModel.query.get(task_id)
        user = userModel.query.get(get_jwt_identity())
        if not task or not user:
            return None

        if user in [x.user for x in task.voting.all()]:
            t = taskVotingModel.query.filter(and_(taskVotingModel.user_id==get_jwt_identity(), taskVotingModel.task_id==task_id)).first()
            t.time = time
            task.time = taskCalcTime(task_id)
            db.session.commit()
            return time

        t = taskVotingModel(user_id=get_jwt_identity(), task_id=task_id, time=time)
        db.session.add(t)
        task.time = taskCalcTime(task_id)
        db.session.commit()

        return time


        




