from flask import Blueprint, request, current_app, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from ..forms import RegisterForm, LoginForm, ProfileForm, AvatarForm, PasswordForm, WalletForm
from ..services import TbUser, TbFile
from ..models import User

address = Blueprint('address', __name__, url_prefix='/addresses')


@address.route('')
def index():
    return 'index'
