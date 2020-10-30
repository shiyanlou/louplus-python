from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for
from flask_login import login_required, current_user
from jobplus.models import Job, Dilivery, db


job = Blueprint('job', __name__, url_prefix='/job')


@job.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.order_by(Job.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('job/index.html', pagination=pagination, active='job')


@job.route('/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html', job=job, active='')


@job.route('/<int:job_id>/apply')
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    if job.current_user_is_applied:
        flash('已经投递过该职位', 'warning')
    else:
        d = Dilivery(
            job_id=job.id,
            user_id=current_user.id
        )
        db.session.add(d)
        db.session.commit()
        flash('投递成功', 'success')
    return redirect(url_for('job.detail', job_id=job.id))
