from flask import Flask, render_template, abort
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
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
