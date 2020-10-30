import pandas as pd
import matplotlib.pyplot as plt

def data_plot():
    data = pd.read_json('user_study.json')
    df = data.groupby('user_id').sum()
    ax = df.plot.line(title='StudyData')
    ax.set_xlabel('User ID')
    ax.set_ylabel('Study Time')
    plt.show()
    return ax

data_plot()
