from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User


def jwt_decorator():
    def f1(fn):
        @wraps(fn)
        def f2(*args, **kwargs):
            verify_jwt_in_request()
            user = User.query.get(get_jwt_identity())
            if not user:
                resp = jsonify({"msg": "User does not exist"})
                resp.status = "401"
                return resp
            if not user.admin:
                resp = jsonify({"msg": "User is not Admin"})
                resp.status = "401"
                return resp
            token = request.headers.get("Authorization")
            if user.token != token and user.old_token != token:
                resp = jsonify({"msg": "Bad token"})
                resp.status = "401"
                return resp
            return fn(*args, **kwargs)
        return f2
    return f1
