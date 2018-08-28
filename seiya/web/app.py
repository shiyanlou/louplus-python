from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/job')
def jobIndex():
    return render_template('job/index.html')


@app.route('/job/count-top10')
def jobCountTop10():
    return render_template('job/count-top10.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
