from flask import Blueprint, request, current_app
from sqlalchemy import or_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import Shop, ShopSchema, Product, ProductSchema

shop = Blueprint('shop', __name__, url_prefix='/shops')


@shop.route('', methods=['POST'])
def create_shop():
    data = request.get_json()

    shop = ShopSchema().load(data)
    session.add(shop)
    session.commit()

    return json_response(shop=ShopSchema().dump(shop))


@shop.route('', methods=['GET'])
def shop_list():
    owner_id = request.args.get('owner_id', 0, type=int)
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Shop.id.asc() if order_direction == 'asc' else Shop.id.desc()
    query = Shop.query
    if owner_id != 0:
        query = query.filter(Shop.owner_id == owner_id)
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(shops=ShopSchema().dump(query, many=True))


@shop.route('/<int:shop_id>', methods=['POST'])
def update_shop(shop_id):
    data = request.get_json()

    count = Shop.query.filter(Shop.id == shop_id).update(data)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    shop = Shop.query.get(shop_id)
    session.commit()

    return json_response(shop=ShopSchema().dump(shop))


@shop.route('/<int:shop_id>', methods=['GET'])
def shop_info(shop_id):
    shop = Shop.query.get(shop_id)
    if shop is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(shop=ShopSchema().dump(shop))
