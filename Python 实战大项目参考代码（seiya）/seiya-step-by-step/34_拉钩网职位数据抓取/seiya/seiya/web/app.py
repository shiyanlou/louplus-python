from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/g2')
def g2():
    return render_template('g2.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
