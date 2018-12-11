from flask import Blueprint, request, current_app
from sqlalchemy import or_

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import Shop, ShopSchema, Product, ProductSchema

shop = Blueprint('shop', __name__, url_prefix='/shops')


@shop.route('', methods=['POST'])
def create_shop():
    """创建店铺
    """

    data = request.get_json()

    shop = ShopSchema().load(data)
    session.add(shop)
    session.commit()

    return json_response(shop=ShopSchema().dump(shop))


@shop.route('', methods=['GET'])
def shop_list():
    """店铺列表，可根据用户 ID 等条件来筛选
    """

    user_id = request.args.get('user_id', type=int)
    keywords = request.args.get('keywords', '')
    order_direction = request.args.get('order_direction', 'desc')
    limit = request.args.get(
        'limit', current_app.config['PAGINATION_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Shop.id.asc() if order_direction == 'asc' else Shop.id.desc()
    query = Shop.query
    if user_id is not None:
        query = query.filter(Shop.user_id == user_id)
    if keywords != '':
        query = query.filter(
            or_(Shop.name.match(keywords), Shop.description.match(keywords)))
    total = query.count()
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(shops=ShopSchema().dump(query, many=True), total=total)


@shop.route('/<int:id>', methods=['POST'])
def update_shop(id):
    """更新店铺
    """

    data = request.get_json()

    count = Shop.query.filter(Shop.id == id).update(data)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    shop = Shop.query.get(id)
    session.commit()

    return json_response(shop=ShopSchema().dump(shop))


@shop.route('/<int:id>', methods=['GET'])
def shop_info(id):
    """查询店铺
    """

    shop = Shop.query.get(id)
    if shop is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(shop=ShopSchema().dump(shop))
