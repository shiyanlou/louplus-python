from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest

from ..db import db
from ..models import User, UserSchema
from .common import json_response, ResponseCode

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/users', methods=['POST'])
def users():
    user = UserSchema().load(request.get_json())

    db.session.add(user)
    db.session.commit()

    return json_response(user=UserSchema().dump(user))


@user.route('/users/<int:user_id>', methods=['GET'])
def index(user_id):
    user = User.query.get(user_id)
    if user is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(user=UserSchema().dump(user))
