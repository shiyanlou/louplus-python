import os
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Length, Email, EqualTo, Required
from jobplus.models import db, User, CompanyDetail, Job


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class RegisterForm(FlaskForm):
    name = StringField('用户名', validators=[Required(), Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('名字已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

    def create_user(self):
        user = User(name=self.name.data,
                    email=self.email.data,
                    password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user


class UserProfileForm(FlaskForm):
    real_name = StringField('姓名', [Required()])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码(不填写保持不变)')
    phone = StringField('手机号')
    work_years = IntegerField('工作年限')
    resume = FileField('上传简历', validators=[FileRequired()])
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('请输入有效的手机号')

    def upload_resume(self):
        f = self.resume.data
        filename = self.real_name.data + '.pdf'
        f.save(os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'static',
            'resumes',
            filename
        ))
        return filename

    def update_profile(self, user):
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        filename = self.upload_resume()
        user.resume_url = url_for('static', filename=os.path.join('resumes', filename))
        db.session.add(user)
        db.session.commit()


class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[Required(), Email()])
    phone = StringField('手机号')
    password = PasswordField('密码(不填写保持不变)')
    slug = StringField('Slug', validators=[Required(), Length(3, 24)])
    location = StringField('地址', validators=[Length(0, 64)])
    site = StringField('公司网站', validators=[Length(0, 64)])
    logo = StringField('Logo')
    description = StringField('一句话描述', validators=[Length(0, 100)])
    about = TextAreaField('公司详情', validators=[Length(0, 1024)])
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('请输入有效的手机号')

    def updated_profile(self, user):
        user.name = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.detail:
            detail = user.detail
        else:
            detail = CompanyDetail()
            detail.user_id = user.id
        self.populate_obj(detail)
        db.session.add(user)
        db.session.add(detail)
        db.session.commit()


class UserEditForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码')
    real_name = StringField('姓名')
    phone = StringField('手机号')
    submit = SubmitField('提交')

    def update(self, user):
        self.populate_obj(user)
        if self.password.data:
            user.password = self.password.data
        db.session.add(user)
        db.session.commit()


class CompanyEditForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码')
    phone = StringField('手机号')
    site = StringField('公司网站', validators=[Length(0, 64)])
    description = StringField('一句话简介', validators=[Length(0, 100)])
    submit = SubmitField('提交')

    def update(self, company):
        company.name = self.name.data
        company.email = self.email.data
        if self.password.data:
            company.password = self.password.data
        if company.detail:
            detail = company.detail
        else:
            detail = CompanyDetail()
            detail.user_id = company.id
        detail.site = self.site.data
        detail.description = self.description.data
        db.session.add(company)
        db.session.add(detail)
        db.session.commit()


class JobForm(FlaskForm):
    name = StringField('职位名称')
    salary_low = IntegerField('最低薪酬')
    salary_high = IntegerField('最高薪酬')
    location = StringField('工作地点')
    tags = StringField('职位标签（多个用,隔开）')
    experience_requirement = SelectField(
        '经验要求(年)',
        choices=[
            ('不限', '不限'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('1-3', '1-3'),
            ('3-5', '3-5'),
            ('5+', '5+')
        ]
    )
    degree_requirement = SelectField(
        '学历要求',
        choices=[
            ('不限', '不限'),
            ('专科', '专科'),
            ('本科', '本科'),
            ('硕士', '硕士'),
            ('博士', '博士')
        ]
    )
    description = TextAreaField('职位描述', validators=[Length(0, 1500)])
    submit = SubmitField('发布')

    def create_job(self, company):
        job = Job()
        self.populate_obj(job)
        job.company_id = company.id
        db.session.add(job)
        db.session.commit()
        return job

    def update_job(self, job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job
