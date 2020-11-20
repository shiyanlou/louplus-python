import pandas as pd

def analysis(file, user_id):
    df = pd.read_json(file)
    s = df[df.user_id==user_id].minutes
    return s.count(), s.sum()
