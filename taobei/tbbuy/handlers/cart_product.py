from flask import Blueprint, request, current_app
from sqlalchemy import and_

from ..db import session
from ..models import CartProduct, CartProductSchema
from .common import json_response, ResponseCode

cart_product = Blueprint('cart_product', __name__, url_prefix='/')


@cart_product.route('/cart_products', methods=['POST'])
def create_cart_product():
    data = request.get_json()

    cart_product = CartProductSchema().load(data)
    session.add(cart_product)
    session.commit()

    return json_response(cart_product=CartProductSchema().dump(cart_product))


@cart_product.route('/cart_products', methods=['GET'])
def cart_product_list():
    user_id = request.args.get('user_id', 0, type=int)
    product_id = request.args.get('product_id', 0, type=int)
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = CartProduct.id.asc(
    ) if order_direction == 'asc' else CartProduct.id.desc()
    query = CartProduct.query
    if user_id > 0:
        query = query.filter(CartProduct.user_id == user_id)
    if product_id > 0:
        query = query.filter(CartProduct.product_id == product_id)
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(favorite_products=CartProductSchema().dump(query, many=True))


@cart_product.route('/cart_products/<int:user_id>/<int:product_id>', methods=['DELETE'])
def delete_cart_product(user_id, product_id):
    cart_product = CartProduct.query.filter(and_(
        CartProduct.user_id == user_id, CartProduct.product_id == product_id)).first()
    if cart_product is None:
        return json_response(ResponseCode.NOT_FOUND)
    session.delete(cart_product)
    session.commit()

    return json_response(cart_product=CartProductSchema().dump(cart_product))


@cart_product.route('/cart_products/<int:user_id>/<int:product_id>', methods=['GET'])
def cart_product_info(user_id, product_id):
    cart_product = CartProduct.query.filter(and_(
        CartProduct.user_id == user_id, CartProduct.product_id == product_id)).first()
    if cart_product is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(cart_product=CartProductSchema().dump(cart_product))
