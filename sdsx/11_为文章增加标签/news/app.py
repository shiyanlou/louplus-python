from flask import Flask, render_template, abort
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
client = MongoClient('127.0.0.1', 27017)
tag = client.shiyanlou.tag

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    def __init__(self, a): 
        self.name = a 
    def __repr__(self):
        return '<Category: {}>'.format(self.name)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime, default=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='file')
    content = db.Column(db.Text)
    def __init__(self, a, b, c): 
        self.title = a 
        self.category = b 
        self.content = c 
    def add_tag(self, tag_name):
        doc = tag.find_one({'id': self.id})
        if doc:
            tags = doc['tags']
            if not tag_name in tags:
                tags.append(tag_name)
                tag.update_one({'id': self.id}, {'$set': {'tags': tags}})
        else:
            tag.insert_one({'id': self.id, 'tags': [tag_name]})
    def remove_tag(self, tag_name):
        doc = tag.find_one({'id': self.id})
        if doc:
            tags = doc['tags']
            if tag_name in tags:
                tags.remove(tag_name)
                doc.update_one({'id': self.id}, {'$set': {'tags': tags}})
    @property
    def tags(self):
        return tag.find_one({'id': self.id})['tags']

    def __repr__(self):
        return '<File: {}>'.formate(self.title)


@app.route('/')
def index():
    return render_template('index.html', l=File.query.all())

@app.route('/files/<file_id>')
def file(file_id):
    f = File.query.get_or_404(file_id)
    return render_template('file.html', f=f)

@app.errorhandler(404)
def not_f(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', java, 'File Content - Java is cool!')
    file2 = File('Hello Python', python, 'File Content - Python is cool!')
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
