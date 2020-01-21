from app import app, jwt
from app import socketio
from flask import request, abort

@app.before_request
def user_loader_callback():

    # return ''
    # print('qwerg')

    request_token = request.headers.get('Authorization')
    type_app = request.headers.get('typeApp')

    # abort(404)


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', debug=True, port='4999')
    # socketio.run(app, debug=True, port='4999')