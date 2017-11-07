from flask import Blueprint, render_template
from simpledu.models import Course, Chapter
from flask_login import login_required

course = Blueprint('course', __name__, url_prefix='/courses')


@course.route('/<int:course_id>')
def index(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course/detail.html', course=course)


@course.route('/<int:course_id>/chapters/<int:chapter_id>')
@login_required
def chapter(course_id, chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template('course/chapter.html', chapter=chapter)


