from flask import Blueprint, request, current_app
from sqlalchemy import and_

from ..db import session
from ..models import OrderProduct, OrderProductSchema
from .common import json_response, ResponseCode

order_product = Blueprint('order_product', __name__, url_prefix='/')


@order_product.route('/order_products', methods=['POST'])
def create_order_product():
    data = request.get_json()

    order_product = OrderProductSchema().load(data)
    session.add(order_product)
    session.commit()

    return json_response(order_product=OrderProductSchema().dump(order_product))


@order_product.route('/order_products', methods=['GET'])
def order_product_list():
    order_id = request.args.get('order_id', 0, type=int)
    product_id = request.args.get('product_id', 0, type=int)
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = OrderProduct.id.asc(
    ) if order_direction == 'asc' else OrderProduct.id.desc()
    query = OrderProduct.query
    if order_id > 0:
        query = query.filter(OrderProduct.order_id == order_id)
    if product_id > 0:
        query = query.filter(OrderProduct.product_id == product_id)
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(favorite_products=OrderProductSchema().dump(query, many=True))


@order_product.route('/order_products/<int:order_id>/<int:product_id>', methods=['DELETE'])
def delete_order_product(order_id, product_id):
    order_product = OrderProduct.query.filter(and_(
        OrderProduct.order_id == order_id, OrderProduct.product_id == product_id)).first()
    if order_product is None:
        return json_response(ResponseCode.NOT_FOUND)
    session.delete(order_product)
    session.commit()

    return json_response(order_product=OrderProductSchema().dump(order_product))


@order_product.route('/order_products/<int:order_id>/<int:product_id>', methods=['GET'])
def order_product_info(order_id, product_id):
    order_product = OrderProduct.query.filter(and_(
        OrderProduct.order_id == order_id, OrderProduct.product_id == product_id)).first()
    if order_product is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(order_product=OrderProductSchema().dump(order_product))
