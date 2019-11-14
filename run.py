from app import app, jwt
from app import socketio

@jwt.user_loader_callback_loader
def user_loader_callback(identity):

    # return ''
    print('qwerg')

    request_token = request.headers['Authorization']
    type_app = request.headers['typeApp']

    abort(404)


if __name__ == '__main__':
    socketio.run(app,host='192.168.100.201', debug=True, port='4999')