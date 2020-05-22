from app import app, api, jwt
from flask_restful import Api, Resource
from app.resources.task import Task
from app.resources.project import Project, ProjectList
from app.resources.user import User
from app.resources.project_user import ProjectUser
from app.resources.protected_user import ProtectedUser
from app.resources.login_from_google import login_from_google_1, login_from_google_2
from app.resources.logout import logout
from app.resources.check_token import check_token
from app.resources.update_token import update_token 
from app.resources.weather import Weather
from app.resources.login import Login

api.add_resource(Weather, '/weather')

api.add_resource(ProjectList, '/project')

api.add_resource(Project, '/project/<int:id>', '/project')

api.add_resource(Task, '/task', '/task/<int:id>')

api.add_resource(User, '/user', '/user/<int:id>')

api.add_resource(ProjectUser, '/project_user', '/project_user/<int:id>')

api.add_resource(ProtectedUser, '/protected_user')

app.route('/update_token')(update_token)

app.route('/check_token')(check_token)

app.route("/login_from_google_1")(login_from_google_1)

app.route("/login_from_google_2")(login_from_google_2)

app.route('/logout')(logout)

api.add_resource(Login,'/login')

