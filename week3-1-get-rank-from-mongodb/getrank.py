import sys
import pandas as pd
from pymongo import MongoClient


def get_rank(user_id):
    # 读取数据
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests
    data = pd.DataFrame(list(contests.find()))
    # 判断 user_id 是否存在
    if user_id in list(data['user_id']):
        # 计算用户 user_id 的排名、总分数及总时间
        group_data = data.groupby(['user_id'])['score', 'submit_time'].sum()
        rank_data = group_data.sort_values(['submit_time']).sort_values([
            'score'], ascending=False)
        reindex_data = rank_data.reset_index()
        reindex_data['rank'] = reindex_data.index + 1
        user_data = reindex_data[reindex_data['user_id'] == user_id]
        rank = int(user_data['rank'].values)
        score = int(user_data['score'].values)
        submit_time = int(user_data['submit_time'].values)
    else:
        print("NOTFOUND")
        exit()

    # 依次返回排名，分数和时间，不能修改顺序
    return rank, score, submit_time


if __name__ == '__main__':
    # 判断参数格式
    if len(sys.argv) != 2:
        print("Parameter error.")
        sys.exit(1)

    # 获取用户 ID
    user_id = sys.argv[1]

    # 根据用户 ID 获取用户排名，分数和时间
    userdata = get_rank(int(user_id))
    print(userdata)
