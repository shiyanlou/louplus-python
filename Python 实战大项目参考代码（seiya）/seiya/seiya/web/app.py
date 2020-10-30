
from flask import Flask, render_template, jsonify, Response

import seiya.analysis.job as job

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    """404 页面

    """
    return render_template('404.html'), 404


@app.route('/')
def index():
    """首页

    """
    return render_template('index.html')


@app.route('/g2')
def g2():
    """G2 图表示例页

    """
    return render_template('g2.html')


@app.route('/job')
def job_index():
    """拉勾网职位数据分析首页

    """
    return render_template('job/index.html')


@app.route('/job/count-top10')
def job_count_top10():
    """职位数排名前十的城市页面

    """
    return render_template('job/count-top10.html', rows=job.count_top10())


@app.route('/job/count-top10.json')
def job_count_top10_json():
    """职位数排名前十的城市数据

    """
    return jsonify(job.count_top10())


@app.route('/job/salary-top10')
def job_salary_top10():
    """薪资排名前十的城市页面

    """
    return render_template('job/salary-top10.html', rows=job.salary_top10())


@app.route('/job/salary-top10.json')
def job_salary_top10_json():
    """薪资排名前十的城市数据

    """
    return jsonify(job.salary_top10())


@app.route('/job/hot-tags')
def job_hot_tags():
    """热门职位标签页面

    """
    return render_template('job/hot-tags.html', rows=job.hot_tags())


@app.route('/job/hot-tags.json')
def job_hot_tags_json():
    """热门职位标签数据

    """
    return jsonify(job.hot_tags())


@app.route('/job/hot-tags.png')
def job_hot_tags_plot():
    """热门职位标签图片

    """
    return Response(job.hot_tags_plot(format='png'), content_type='image/png')


@app.route('/job/experience-stat')
def job_experience_stat():
    """工作经验统计页面

    """
    return render_template('job/experience-stat.html', rows=job.experience_stat())


@app.route('/job/experience-stat.json')
def job_experience_stat_json():
    """工作经验统计数据

    """
    return jsonify(job.experience_stat())


@app.route('/job/education-stat')
def job_education_stat():
    """学历要求统计页面

    """
    return render_template('job/education-stat.html', rows=job.education_stat())


@app.route('/job/education-stat.json')
def job_education_stat_json():
    """学历要求统计数据

    """
    return jsonify(job.education_stat())


@app.route('/job/salary-by-city-and-education')
def job_salary_by_city_and_education():
    """同等学历不同城市薪资对比页面

    """
    return render_template('job/salary-by-city-and-education.html',
                           rows=job.salary_by_city_and_education())


@app.route('/job/salary-by-city-and-education.json')
def job_salary_by_city_and_education_json():
    """同等学历不同城市薪资对比数据

    """
    return jsonify(job.salary_by_city_and_education())


if __name__ == '__main__':
    app.run()
