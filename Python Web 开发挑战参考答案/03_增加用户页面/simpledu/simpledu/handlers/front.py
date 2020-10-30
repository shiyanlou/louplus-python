from flask import Blueprint, render_template
from simpledu.models import Course


front = Blueprint('front', __name__)


@front.route('/')
def index():
    """首页"""

    courses = Course.query.all()
    return render_template('index.html', courses=courses)
