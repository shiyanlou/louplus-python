from flask import Blueprint, request, current_app
from sqlalchemy import or_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import Order, OrderSchema, OrderProduct, OrderProductSchema

order = Blueprint('order', __name__, url_prefix='/orders')


@order.route('', methods=['POST'])
def create_order():
    """创建订单，订单商品需要一起提交
    """

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
    """订单列表
    """

    user_id = request.args.get('user_id', type=int)
    order_direction = request.args.get('order_direction', 'desc')
    limit = request.args.get(
        'limit', current_app.config['PAGINATION_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Order.id.asc() if order_direction == 'asc' else Order.id.desc()
    query = Order.query
    if user_id is not None:
        query = query.filter(Order.user_id == user_id)
    total = query.count()
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(orders=OrderSchema().dump(query, many=True), total=total)


@order.route('/<int:id>', methods=['POST'])
def update_order(id):
    """更新订单，支持部分更新，但只能更新地址、备注、状态都信息
    注意订单商品要么不更新，要么整体一起更新
    """

    data = request.get_json()

    order = Order.query.get(id)
    if order is None:
        return json_response(ResponseCode.NOT_FOUND)
    if data.get('address_id') is not None:
        order.address_id = data.get('address_id')
    if data.get('note') is not None:
        order.note = data.get('note')
    if data.get('status') is not None:
        order.status = data.get('status')

    if data.get('order_products') is not None:
        order_products = []
        for op in data.get('order_products'):
            order_product = OrderProduct.query.get(op.get('id'))
            if order_product is None:
                return json_response(ResponseCode.NOT_FOUND)
            if op.get('amount') is not None:
                order_product.amount = op.get('amount')
            if op.get('price') is not None:
                order_product.price = op.get('price')
            order_products.append(order_product)
        order.order_products = order_products

    session.commit()

    return json_response(order=OrderSchema().dump(order))


@order.route('/<int:id>', methods=['GET'])
def order_info(id):
    """查询订单
    """

    order = Order.query.get(id)
    if order is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(order=OrderSchema().dump(order))
