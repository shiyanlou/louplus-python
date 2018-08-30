from sqlalchemy import func, Float, select
import pandas as pd

from seiya.db import engine, Session, JobModel


def count_top10():
    session = Session()
    rows = session.query(
        func.count(JobModel.city).label('count'), JobModel.city
    ).group_by(JobModel.city).order_by('count desc').limit(10)
    return [row._asdict() for row in rows]


def salary_top10():
    session = Session()
    rows = session.query(
        func.avg(
            (JobModel.salary_lower + JobModel.salary_upper) / 2
        ).cast(Float).label('salary'),
        JobModel.city
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
