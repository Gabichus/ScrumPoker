from flask_jwt_extended import jwt_required
from flask import jsonify


def check_token():
    return jsonify(msg="Success"), 200