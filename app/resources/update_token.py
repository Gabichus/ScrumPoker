from flask import jsonify
from app import db
from app.models import User
from threading import Timer
from flask_jwt_extended import get_jwt_identity, create_access_token
from app.common.jwt_decorator import jwt_decorator
from flask_jwt_extended import jwt_required


def del_old_token(user_id):
    user = User.query.get(user_id)
    user.old_token = None
    db.session.commit()


# @my_jwt_required()
@jwt_required
def update_token():
    user = User.query.get(get_jwt_identity())
    user.old_token = user.token
    del_timer = Timer(300, del_old_token, [user.id])  # старый токен будет валиден ещё 5 мин
    del_timer.start()
    user.token = create_access_token(get_jwt_identity())
    db.session.commit()
    return jsonify(token=user.token), 200
