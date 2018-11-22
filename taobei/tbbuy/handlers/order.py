from flask import Blueprint, request, current_app
from sqlalchemy import or_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import Order, OrderSchema

order = Blueprint('order', __name__, url_prefix='/orders')


@order.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    if data.get('pay_amount') is None:
        data['pay_amount'] = sum([x['price'] * x['amount']
                                  for x in data['order_products']])

    order = OrderSchema().load(data)
    session.add(order)
    session.commit()

    return json_response(order=OrderSchema().dump(order))


@order.route('', methods=['GET'])
def order_list():
    user_id = request.args.get('user_id', 0, type=int)
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Order.id.asc() if order_direction == 'asc' else Order.id.desc()
    query = Order.query
    if user_id > 0:
        query = query.filter(Order.user_id == user_id)
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(orders=OrderSchema().dump(query, many=True))


@order.route('/<int:order_id>', methods=['POST'])
def update_order(order_id):
    data = request.get_json()

    count = Order.query.filter(Order.id == order_id).update(data)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    order = Order.query.get(order_id)
    session.commit()

    return json_response(order=OrderSchema().dump(order))


@order.route('/<int:order_id>', methods=['GET'])
def order_info(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(order=OrderSchema().dump(order))
