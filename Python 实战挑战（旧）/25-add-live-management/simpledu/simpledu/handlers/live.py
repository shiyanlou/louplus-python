from flask import Blueprint, render_template
from simpledu.models import Live

live = Blueprint('live', __name__, url_prefix='/live')


@live.route('/')
def index():
    # 获取最新的一个直播
    live = Live.query.order_by(Live.created_at.desc()).limit(1).first()
    return render_template('live/index.html', live=live)
