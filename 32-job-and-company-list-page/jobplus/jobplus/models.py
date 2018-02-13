from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Base(db.Model):
    """ 所有 model 的一个基类，默认添加了时间戳
    """
    # 表示不要把这个类当作 Model 类
    __abstract__ = True
    # 设置了 defautl 和 onupdate 这俩个时间戳都不需要自己去维护
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)


user_job = db.Table(
    'user_job',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
)


class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    real_name = db.Column(db.String(20))
    phone = db.Column(db.String(11))
    work_years = db.Column(db.SmallInteger)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    # 根据用户在网站上填写的内容生成的简历
    resume = db.relationship('Resume', uselist=False)
    collect_jobs = db.relationship('Job', secondary=user_job)
    # 用户上传的简历或者简历链接
    resume_url = db.Column(db.String(64))

    # 企业用户详情
    detail = db.relationship('CompanyDetail', uselist=False)

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_staff(self):
        return self.role == self.ROLE_USER


class Resume(Base):
    __tablename__ = 'resume'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False)
    job_experiences = db.relationship('JobExperience')
    edu_experiences = db.relationship('EduExperience')
    project_experiences = db.relationship('ProjectExperience')

    def profile(self):
        pass


class Experience(Base):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    begin_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    # 在职期间，做了什么，解决了什么问题，做出了什么贡献
    # 在校期间做过什么，取得过什么荣誉
    # 项目期间，做了什么，解决了什么问题，做出了什么贡献
    description = db.Column(db.String(1024))


class JobExperience(Experience):
    __tablename__ = 'job_experience'

    company = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


class EduExperience(Experience):
    __tablename__ = 'edu_experience'

    school = db.Column(db.String(32), nullable=False)
    # 所学专业
    specialty = db.Column(db.String(32), nullable=False)
    degree = db.Column(db.String(16))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


class ProjectExperience(Experience):
    __tablename__ = 'preject_experience'

    name = db.Column(db.String(32), nullable=False)
    # 在项目中扮演的角色
    role = db.Column(db.String(32))
    # 多个技术用逗号隔开
    technologys = db.Column(db.String(64))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


class CompanyDetail(Base):
    __tablename__ = 'company_detail'

    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(256), nullable=False)
    site = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(24), nullable=False)
    # 一句话描述
    description = db.Column(db.String(100))
    # 关于我们，公司详情描述
    about = db.Column(db.String(1024))
    # 公司标签，多个标签用逗号隔开，最多10个
    tags = db.Column(db.String(128))
    # 公司技术栈，多个技术用逗号隔开，最多10个
    stack = db.Column(db.String(128))
    # 团队介绍
    team_introduction = db.Column(db.String(256))
    # 公司福利，多个福利用分号隔开，最多 10 个
    welfares = db.Column(db.String(256))
    # 公司领域
    field = db.Column(db.String(128))
    # 融资进度
    finance_stage = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', uselist=False, backref=db.backref('company_detail', uselist=False))

    def __repr__(self):
        return '<CompanyDetail {}>'.format(self.id)


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    # 职位名称
    name = db.Column(db.String(24))
    salary_low = db.Column(db.Integer, nullable=False)
    salary_high = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(24))
    # 职位标签，多个标签用逗号隔开，最多10个
    tags = db.Column(db.String(128))
    experience_requirement = db.Column(db.String(32))
    degree_requirement = db.Column(db.String(32))
    is_fulltime = db.Column(db.Boolean, default=True)
    # 是否在招聘
    is_open = db.Column(db.Boolean, default=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    company = db.relationship('User', uselist=False, backref=db.backref('jobs', lazy='dynamic'))
    views_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Job {}>'.format(self.name)

    @property
    def tag_list(self):
        return self.tags.split(',')


class Dilivery(Base):
    __tablename__ = 'delivery'

    # 等待企业审核
    STATUS_WAITING = 1
    # 被拒绝
    STATUS_REJECT = 2
    # 被接收，等待通知面试
    STATUS_ACCEPT = 3

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    status = db.Column(db.SmallInteger, default=STATUS_WAITING)
    # 企业回应
    response = db.Column(db.String(256))
