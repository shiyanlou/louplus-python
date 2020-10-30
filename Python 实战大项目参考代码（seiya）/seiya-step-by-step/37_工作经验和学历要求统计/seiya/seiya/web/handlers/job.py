from flask import render_template, Blueprint, Response, jsonify
import seiya.analysis.job as job_

job = Blueprint('job', __name__, url_prefix='/job')

# 拉勾网职位数据分析首页
@job.route('/')
def index():
    return render_template('job/index.html')

# 职位数量排名前十的城市
@job.route('/count_top10')
def count_top10():
    return render_template('job/count_top10.html', query=job_.count_top10())

# 平均薪资排名前十的城市
@job.route('/salary_top10')
def salary_top10():
    return render_template('job/salary_top10.html', query=job_.salary_top10())

# 数量排名前十的热门标签
@job.route('/hot_tags')
def hot_tags():
    query = [{'tag': i, 'count': j} for i, j in job_.hot_tags().items()]
    return render_template('job/hot_tags.html', query=query)

# 数量排名前十的热门标签图片
@job.route('/hot_tags.png')
def hot_tags_plot():
    # Response 是将数据直接发送给浏览器，不需要前端模板了
    # 这里就是将一张图的数据直接发送给浏览器
    return Response(job_.hot_tags_plot(), content_type='image/png')

# 数量排名前十的热门标签 JSON 数据
@job.route('/hot_tags.json')
def hot_tags_json():
    d = {key: int(value) for key, value in job_.hot_tags().to_dict().items()}
    return jsonify(d)

# 工作经验统计
@job.route('/experience_stat')
def experience_stat():
    return render_template('job/experience_stat.html', rows=job_.experience_stat())

# 工作经验统计 JSON 格式
@job.route('/experience_stat.json')
def experience_stat_json():
    return jsonify(job_.experience_stat())

# 学历要求统计
@job.route('/education_stat')
def education_stat():
    return render_template('job/education_stat.html', rows=job_.education_stat())

# 学历要求统计 JSON 格式
@job.route('/education_stat.json')
def education_stat_json():
    return jsonify(job_.education_stat())
