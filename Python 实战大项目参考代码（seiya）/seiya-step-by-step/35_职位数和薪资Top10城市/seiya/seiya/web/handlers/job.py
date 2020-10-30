from flask import render_template, Blueprint, url_for, redirect
import seiya.analysis.job as job_

job = Blueprint('job', __name__, url_prefix='/job')

@job.route('/')
def index():
    return render_template('job/index.html')

@job.route('/count_top10')
def count_top10():
    return render_template('job/count_top10.html', query=job_.count_top10())

@job.route('/salary_top10')
def salary_top10():
    return render_template('job/salary_top10.html', query=job_.salary_top10())
