from flask import Blueprint, request, current_app
from sqlalchemy import or_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import User, UserSchema, Address, AddressSchema, WalletTransaction, WalletTransactionSchema

user = Blueprint('user', __name__, url_prefix='/users')


@user.route('', methods=['POST'])
def create_user():
    data = request.get_json()

    user = UserSchema().load(data)
    session.add(user)
    session.commit()

    return json_response(user=UserSchema().dump(user))


@user.route('', methods=['GET'])
def user_list():
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = User.id.asc() if order_direction == 'asc' else User.id.desc()
    query = User.query.order_by(order_by).limit(limit).offset(offset)

    return json_response(users=UserSchema().dump(query, many=True))


@user.route('/<int:user_id>', methods=['POST'])
def update_user(user_id):
    data = request.get_json()

    count = User.query.filter(User.id == user_id).update(data)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    user = User.query.get(user_id)
    session.commit()

    return json_response(user=UserSchema().dump(user))


@user.route('/<int:user_id>', methods=['GET'])
def user_info(user_id):
    user = User.query.get(user_id)
    if user is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(user=UserSchema().dump(user))
