from flask import Blueprint, request, current_app
from sqlalchemy import or_

from ..db import session
from ..models import User, UserSchema, Address, AddressSchema, WalletTransaction, WalletTransactionSchema
from .common import json_response, ResponseCode

user = Blueprint('user', __name__, url_prefix='/')


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

    query = User.query.limit(limit).offset(offset)

    return json_response(users=UserSchema().dump(query.all(), many=True))


@user.route('/users/<int:user_id>', methods=['POST'])
def update_user(user_id):
    values = request.get_json()

    count = User.query.filter(User.id == user_id).update(values)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    user = User.query.get(user_id)
    session.commit()

    return json_response(user=UserSchema().dump(user))


@user.route('/users/<int:user_id>', methods=['GET'])
def user_info(user_id):
    user = User.query.get(user_id)
    if user is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(user=UserSchema().dump(user))


@user.route('/users/<int:user_id>/addresses', methods=['GET'])
def addresses_of_user(user_id):
    query = Address.query.filter(Address.owner_id == user_id)

    return json_response(addresses=AddressSchema().dump(query.all(), many=True))


@user.route('/users/<int:user_id>/wallet_transactions', methods=['GET'])
def wallet_transactions_of_user(user_id):
    query = WalletTransaction.query.filter(
        or_(WalletTransaction.payer_id == user_id, WalletTransaction.payee_id == user_id))

    return json_response(wallet_transactions=WalletTransactionSchema().dump(query.all(), many=True))
