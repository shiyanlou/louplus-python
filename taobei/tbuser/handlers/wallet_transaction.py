from flask import Blueprint, request, current_app
from sqlalchemy import and_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import WalletTransaction, WalletTransactionSchema, User

wallet_transaction = Blueprint('wallet_transaction', __name__, url_prefix='/')


@wallet_transaction.route('/wallet_transactions', methods=['POST'])
def create_wallet_transaction():
    data = request.get_json()

    wallet_transaction = WalletTransactionSchema().load(data)

    # 采用乐观锁来防止并发情况下可能出现的数据不一致性，也可使用悲观锁（query 时使用 with_for_update），但资源消耗较大
    payer = User.query.get(wallet_transaction.payer_id)
    if payer is None:
        return json_response(ResponseCode.NOT_FOUND)
    payee = User.query.get(wallet_transaction.payee_id)
    if payee is None:
        return json_response(ResponseCode.NOT_FOUND)
    count = User.query.filter(
        and_(User.id == payer.id, User.wallet_money >= wallet_transaction.amount,
             User.wallet_money == payer.wallet_money)
    ).update({
        User.wallet_money: payer.wallet_money - wallet_transaction.amount
    })
    if count == 0:
        session.rollback()
        return json_response(ResponseCode.TRANSACTION_FAILURE)
    count = User.query.filter(
        and_(User.id == payee.id, User.wallet_money == payee.wallet_money)
    ).update({
        User.wallet_money: payee.wallet_money + wallet_transaction.amount
    })
    if count == 0:
        session.rollback()
        return json_response(ResponseCode.TRANSACTION_FAILURE)

    session.add(wallet_transaction)

    session.commit()

    return json_response(wallet_transaction=WalletTransactionSchema().dump(wallet_transaction))


@wallet_transaction.route('/wallet_transactions', methods=['GET'])
def wallet_transaction_list():
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = WalletTransaction.id.asc(
    ) if order_direction == 'asc' else WalletTransaction.id.desc()
    query = WalletTransaction.query.order_by(
        order_by).limit(limit).offset(offset)

    return json_response(wallet_transactions=WalletTransactionSchema().dump(query, many=True))


@wallet_transaction.route('/wallet_transactions/<int:wallet_transaction_id>', methods=['POST'])
def update_wallet_transaction(wallet_transaction_id):
    data = request.get_json()

    count = WalletTransaction.query.filter(
        WalletTransaction.id == wallet_transaction_id).update(data)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    wallet_transaction = WalletTransaction.query.get(wallet_transaction_id)
    session.commit()

    return json_response(wallet_transaction=WalletTransactionSchema().dump(wallet_transaction))


@wallet_transaction.route('/wallet_transactions/<int:wallet_transaction_id>', methods=['GET'])
def wallet_transaction_info(wallet_transaction_id):
    wallet_transaction = WalletTransaction.query.get(wallet_transaction_id)
    if wallet_transaction is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(wallet_transaction=WalletTransactionSchema().dump(wallet_transaction))
