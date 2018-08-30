from flask import Flask, render_template, jsonify

import seiya.web.job as job

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/job')
def job_index():
    return render_template('job/index.html')


@app.route('/job/count-top10')
def job_count_top10():
    return render_template('job/count-top10.html', rows=job.count_top10())


@app.route('/job/count-top10.json')
def job_count_top10_json():
    return jsonify(job.count_top10())


@app.route('/job/salary-top10')
def job_salary_top10():
    return render_template('job/salary-top10.html', rows=job.salary_top10())


@app.route('/job/salary-top10.json')
def job_salary_top10_json():
    return jsonify(job.salary_top10())


@app.route('/job/hot-tags')
def job_hot_tags():
    return render_template('job/hot-tags.html', rows=job.hot_tags())


@app.route('/job/hot-tags.json')
def job_hot_tags_json():
    return jsonify(job.hot_tags())


if __name__ == '__main__':
    app.run()
