from sqlalchemy import func

from seiya.db import Session, JobModel


def count_top10():
    session = Session()
    return session.query(func.count(JobModel.city), JobModel.city).group_by(
        JobModel.city).order_by(func.count(JobModel.city).desc()).limit(10).all()
