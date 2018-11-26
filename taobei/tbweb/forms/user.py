from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email, EqualTo, DataRequired, ValidationError

from ..services import TbUser


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField(
        '重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self, field):
        resp = TbUser(current_app).get_json('/users', params={
            'username': field.data,
        })
        if len(resp['data']['users']) > 0:
            raise ValidationError('用户名已经存在')

    def create_user(self):
        resp = TbUser(current_app).post_json('/users', {
            'username': self.username.data,
            'password': self.password.data,
        })
        return resp['data']['user']


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_password(self, field):
        resp = TbUser(current_app).get_json('/users/check_password', params={
            'username': self.username.data,
            'password': field.data,
        })
        if not resp['data']['isCorrect']:
            raise ValidationError('用户名或密码错误')
