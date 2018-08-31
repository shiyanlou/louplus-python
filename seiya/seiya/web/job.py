from sqlalchemy import func, Float, select, and_
import pandas as pd

from seiya.db import engine, Session, JobModel


def count_top10():
    session = Session()
    rows = session.query(
        JobModel.city,
        func.count(JobModel.city).label('count')
    ).group_by(JobModel.city).order_by('count desc').limit(10)
    return [row._asdict() for row in rows]


def salary_top10():
    session = Session()
    rows = session.query(
        JobModel.city,
        func.avg(
            (JobModel.salary_lower + JobModel.salary_upper) / 2
        ).cast(Float).label('salary')
    ).group_by(JobModel.city).order_by('salary desc').limit(10)
    return [row._asdict() for row in rows]


def hot_tags():
    df = pd.read_sql(select([JobModel.tags]), engine)

    df = pd.concat([pd.Series(row['tags'].split(' '))
                    for _, row in df.iterrows()]).reset_index()
    del df['index']
    df.columns = ['tag']

    df = df[df['tag'] != '""']
    df = df[df['tag'] != '']

    s = df.groupby(['tag']).size().sort_values(ascending=False)

    rows = []
    for item in s.items():
        rows.append({'tag': item[0], 'count': item[1]})

    return rows


def experience_stat():
    session = Session()
    rows = session.query(
        func.concat(
            JobModel.experience_lower, '-', JobModel.experience_upper, '年'
        ).label('experience'),
        func.count('experience').label('count')
    ).group_by('experience').order_by('count desc')
    return [row._asdict() for row in rows]


def education_stat():
    session = Session()
    rows = session.query(
        JobModel.education,
        func.count(JobModel.education).label('count')
    ).group_by('education').order_by('count desc')
    return [row._asdict() for row in rows]


def salary_by_city_and_education():
    session = Session()
    rows = session.query(
        JobModel.city,
        JobModel.education,
        func.avg(
            (JobModel.salary_lower + JobModel.salary_upper) / 2
        ).cast(Float).label('salary')
    ).filter(
        and_(JobModel.salary_lower > 0, JobModel.salary_upper > 0)
    ).group_by(JobModel.city, JobModel.education).order_by(JobModel.city.desc())
    return [row._asdict() for row in rows]
