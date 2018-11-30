from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import Required, Optional, Length, Email, EqualTo, DataRequired, ValidationError, NumberRange

from ..services import TbUser


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(2, 20)])
    password = PasswordField('密码', validators=[Required(), Length(6, 20)])
    repeat_password = PasswordField(
        '重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self, field):
        resp = TbUser(current_app).get_json('/users', params={
            'username': field.data,
        })
        if len(resp['data']['users']) > 0:
            raise ValidationError('用户名已经存在')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(2, 20)])
    password = PasswordField('密码', validators=[Required(), Length(6, 20)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')


class ProfileForm(FlaskForm):
    username = StringField('用户名', validators=[Length(2, 20)])
    gender = StringField('性别', validators=[Length(1, 1)])
    mobile = StringField('手机', validators=[Length(11, 11)])
    submit = SubmitField('提交')


class AvatarForm(FlaskForm):
    avatar = FileField(
        validators=[FileRequired(), FileAllowed(['jpg', 'png'], '头像必须为图片')])
    submit = SubmitField('提交')


class PasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[Required(), Length(6, 20)])
    repeat_password = PasswordField(
        '重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')


class WalletForm(FlaskForm):
    money = IntegerField('充值数量（元）', validators=[
                         Required(), NumberRange(1, 1000000)])
    submit = SubmitField('提交')
