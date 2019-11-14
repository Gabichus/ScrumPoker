from app import app, api
from flask_restful import Api, Resource
from app.resources.task import Task
from app.resources.project import Project, ProjectList
from app.resources.user import User
from app.resources.login_from_google import login_from_google_1, login_from_google_2
from app.resources.logout import logout


api.add_resource(ProjectList, '/project')

api.add_resource(Project, '/project/<int:id>', '/project')

api.add_resource(Task, '/task', '/task/<int:id>')

api.add_resource(User, '/user')

app.route("/login_from_google_1")(login_from_google_1)

app.route("/login_from_google_2")(login_from_google_2)

app.route('/logout')(logout)




# class MessageWsServer(Namespace):
#     def on_connect(self):
#         print('conect')
#         pass

#     def on_disconnect(self):
#         print('disconect')
#         pass

#     def on_team(self, data):
#         print('Daaaataa team', data)
#         # num = data['team_id']
#         # self.emit('team'+str(num), data=data)

#     def on_test(self, data):
#         print('---------Daaaataa-------------', data)
#         # num = data['msg']['team_id']
#         # self.emit('team'+str(num), data=data)

# socketio.on_namespace(MessageWsServer('/lesson'))


from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

class TestRoute(Resource):
    @jwt_required
    def get(self):

        return {'aa':'HopHeyLalaLey'}

    def post(self):

        # emit('my response', json, namespace='/chat')
        return 'post'

api.add_resource(TestRoute, '/test')