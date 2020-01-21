from flask import jsonify
from app import db
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required
def logout():
    user = User.query.get(get_jwt_identity())
    user.old_token = None
    user.token = None
    db.session.commit()
    return jsonify("Success"), 200
