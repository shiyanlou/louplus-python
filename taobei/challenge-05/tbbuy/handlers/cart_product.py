from flask import Blueprint, request, current_app
from sqlalchemy import and_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import CartProduct, CartProductSchema

cart_product = Blueprint('cart_product', __name__, url_prefix='/cart_products')


@cart_product.route('', methods=['POST'])
def create_cart_product():
    """添加购物车商品
    """

    data = request.get_json()

    cart_product = CartProductSchema().load(data)

    cart_products = CartProduct.query.filter(
        CartProduct.user_id == cart_product.user_id).all()

    # 商品是否已在购物车
    existed = None
    for v in cart_products:
        if v.product_id == cart_product.product_id:
            existed = v
            break

    # 购物车商品数量不能超过限制
    if len(cart_products) >= current_app.config['CART_PRODUCT_LIMIT'] and existed is None:
        return json_response(ResponseCode.QUANTITY_EXCEEDS_LIMIT)

    # 商品已在购物车则更新数量，否则添加一条新纪录
    if existed is None:
        session.add(cart_product)
    else:
        existed.amount += cart_product.amount
    session.commit()

    return json_response(cart_product=CartProductSchema().dump(cart_product if existed is None else existed))


@cart_product.route('', methods=['GET'])
def cart_product_list():
    """购物车商品列表
    """

    user_id = request.args.get('user_id', type=int)
    product_id = request.args.get('product_id', type=int)
    order_direction = request.args.get('order_direction', 'desc')

    order_by = CartProduct.id.asc(
    ) if order_direction == 'asc' else CartProduct.id.desc()
    query = CartProduct.query
    if user_id is not None:
        query = query.filter(CartProduct.user_id == user_id)
    if product_id is not None:
        query = query.filter(CartProduct.product_id == product_id)
    total = query.count()
    query = query.order_by(order_by)

    return json_response(cart_products=CartProductSchema().dump(query, many=True), total=total)


@cart_product.route('', methods=['DELETE'])
def delete_cart_products():
    """清空某个用户的购物车商品
    """

    user_id = request.args.get('user_id', type=int)

    CartProduct.query.filter(CartProduct.user_id == user_id).delete()
    session.commit()

    return json_response()


@cart_product.route('/<int:id>', methods=['POST'])
def update_cart_product(id):
    """更新购物车商品，比如数量
    """

    data = request.get_json()

    count = CartProduct.query.filter(CartProduct.id == id).update(data)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    cart_product = CartProduct.query.get(id)
    session.commit()

    return json_response(cart_product=CartProductSchema().dump(cart_product))


@cart_product.route('/<int:id>', methods=['GET'])
def cart_product_info(id):
    """查询购物车商品
    """

    cart_product = CartProduct.query.filter(CartProduct.id == id).first()
    if cart_product is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(cart_product=CartProductSchema().dump(cart_product))


@cart_product.route('/<int:id>', methods=['DELETE'])
def delete_cart_product(id):
    """删除购物车商品
    """

    cart_product = CartProduct.query.filter(CartProduct.id == id).first()
    if cart_product is None:
        return json_response(ResponseCode.NOT_FOUND)

    session.delete(cart_product)
    session.commit()

    return json_response(cart_product=CartProductSchema().dump(cart_product))
