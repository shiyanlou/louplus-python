from flask import Blueprint, request, current_app

from ..db import session
from ..models import WalletTransaction, WalletTransactionSchema
from .common import json_response, ResponseCode

wallet_transaction = Blueprint('wallet_transaction', __name__, url_prefix='/')


@wallet_transaction.route('/wallet_transactions', methods=['POST'])
def create_wallet_transaction():
    wallet_transaction = WalletTransactionSchema().load(request.get_json())

    session.add(wallet_transaction)
    session.commit()

    return json_response(wallet_transaction=WalletTransactionSchema().dump(wallet_transaction))


@wallet_transaction.route('/wallet_transactions', methods=['GET'])
def wallet_transaction_list():
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    query = session.query(WalletTransaction).limit(limit).offset(offset)

    return json_response(wallet_transactions=WalletTransactionSchema().dump(query.all(), many=True))


@wallet_transaction.route('/wallet_transactions/<int:wallet_transaction_id>', methods=['POST'])
def update_wallet_transaction(wallet_transaction_id):
    values = request.get_json()

    count = session.query(WalletTransaction).filter(
        WalletTransaction.id == wallet_transaction_id).update(values)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    wallet_transaction = session.query(
        WalletTransaction).get(wallet_transaction_id)
    session.commit()

    return json_response(wallet_transaction=WalletTransactionSchema().dump(wallet_transaction))


@wallet_transaction.route('/wallet_transactions/<int:wallet_transaction_id>', methods=['GET'])
def wallet_transaction_info(wallet_transaction_id):
    wallet_transaction = session.query(
        WalletTransaction).get(wallet_transaction_id)
    if wallet_transaction is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(wallet_transaction=WalletTransactionSchema().dump(wallet_transaction))
