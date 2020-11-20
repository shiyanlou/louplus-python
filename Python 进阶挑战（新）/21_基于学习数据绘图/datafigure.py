import pandas as pd
import matplotlib.pyplot as plt

def read_json():
    data = pd.read_json('user_study.json')
    df = data.groupby('user_id').sum()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('StudyData')
    ax.set_xlabel('User ID')
    ax.set_ylabel('Study Time')
    ax.plot(df.index, df.minutes)
    plt.show()
    return ax
