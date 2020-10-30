from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import event
from pymongo import MongoClient
from datetime import datetime


db = SQLAlchemy()


app = Flask(__name__)

app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'mysql://root@127.0.0.1/news',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})

db.init_app(app)

# 生成 mongo 客户端，并选择 news 数据库
mongo = MongoClient('127.0.0.1', 27017).news


class File(db.Model):

    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    content = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship('Category', uselist=False)

    def add_tag(self, tag):
        mongo.file.update_one({'_id': self.id}, {'$addToSet': {'tags': tag}})
        return self.__file['tags']

    def remove_tag(self, tag):
        mongo.file.update_one({'_id': self.id}, {'$pull': {'tags': tag}})
        return self.__file['tags']

    @property
    def __file(self):
        return mongo.file.find_one({'_id': self.id})

    @property
    def tags(self):
        return self.__file['tags']


# File 对象插入数据库时，自动创建关联的 Mongodb 对象
@event.listens_for(File, 'after_insert')
def auto_create_mongodb_file(mapper, conn, file):
    mongo.file.insert_one({'_id': file.id})


# File 对象从数据库删除，自动删除关联的 Mongodb 对象
@event.listens_for(File, 'after_delete')
def auto_delete_mongodb_file(mapper, conn, file):
    mongo.file.delete_one({'_id': file.id})


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship('File')

    def __init__(self, name):
        self.name = name


@app.route('/')
@app.route('/files/')
def index():
    return render_template('index.html', files=File.query.all())


@app.route('/files/<int:file_id>')
def file(file_id):
    file = File.query.get_or_404(file_id)
    return render_template('file.html', file=file)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


def insert_datas():
    java = Category('Java')
    python = Category('Python')
    file1 = File(title='Hello Java', category=java,
                 content='File Content - Java is cool!')
    file2 = File(title='Hello Python', category=python,
                 content='File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')


if __name__ == '__main__':
    # 创建数据库
    db.create_all()
    if not Category.query.filter_by(name='Java').first():
        insert_datas()
    app.run()
