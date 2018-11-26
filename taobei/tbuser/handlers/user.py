from flask import Blueprint, request, current_app
from sqlalchemy import or_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import User, UserSchema, Address, AddressSchema, WalletTransaction, WalletTransactionSchema

user = Blueprint('user', __name__, url_prefix='/users')


@user.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    password = data.pop('password')

    user = UserSchema().load(data)
    user.password = password
    session.add(user)
    session.commit()

    return json_response(user=UserSchema().dump(user))


@user.route('', methods=['GET'])
def user_list():
    username = request.args.get('username')
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['PAGINATION_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = User.id.asc() if order_direction == 'asc' else User.id.desc()
    query = User.query
    if username is not None:
        query = query.filter(User.username == username)
    total = query.count()
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(users=UserSchema().dump(query, many=True), total=total)


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


@user.route('/check_password', methods=['GET'])
def check_password():
    username = request.args.get('username')
    password = request.args.get('password')
    if username is None or password is None:
        return json_response(isCorrect=False)

    user = User.query.filter(User.username == username).first()
    if user is None:
        return json_response(isCorrect=False)

    return json_response(isCorrect=user.check_password(password))
