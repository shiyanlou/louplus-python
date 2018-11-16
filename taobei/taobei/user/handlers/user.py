from flask import Blueprint, request, current_app

from ..db import session
from ..models import User, UserSchema
from .common import json_response, ResponseCode

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/users', methods=['POST'])
def create_user():
    user = UserSchema().load(request.get_json())

    session.add(user)
    session.commit()

    return json_response(user=UserSchema().dump(user))


@user.route('/users', methods=['GET'])
def user_list():
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    query = session.query(User).limit(limit).offset(offset)

    return json_response(users=UserSchema().dump(query.all(), many=True))


@user.route('/users/<int:user_id>', methods=['POST'])
def update_user(user_id):
    count = session.query(User).filter(
        User.id == user_id).update(request.get_json())
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)

    session.commit()

    user = session.query(User).get(user_id)

    return json_response(user=UserSchema().dump(user))


@user.route('/users/<int:user_id>', methods=['GET'])
def user_info(user_id):
    user = session.query(User).get(user_id)
    if user is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(user=UserSchema().dump(user))
