import os
import pandas as pd
import numpy as np

def load_data(folder='data', base_filename='combined_data_%d.txt', num_files=4, col_names=['user_id', 'rating']):
    if not os.path.exists(folder):
        raise Exception("No folder '%s' found" % folder)

    user_id = col_names[0]
    ratings = col_names[1]
    
    data = pd.DataFrame()
    for i in range(1,num_files+1):
        path = os.path.join(folder, base_filename % i)
        if not os.path.isfile(path):
            raise Exception("File '%s' not found" % path)
        df = pd.read_csv(path, header=None, names=col_names, usecols=[0, 1])
        df[ratings] = df[ratings].astype(float)
        data = data.append(df)
    data.index = np.arange(0, len(data))

    # Set movie_id column
    df_nan = pd.DataFrame(pd.isnull(data[ratings]))
    df_nan = df_nan[df_nan[ratings] == True]
    df_nan = df_nan.reset_index()
    movie_np = []
    movie_id = 1
    for i,j in zip(df_nan['index'][1:], df_nan['index'][:-1]):
        temp = np.full((1,i-j-1), movie_id)
        movie_np = np.append(movie_np, temp)
        movie_id += 1
    last_record = np.full((1,len(data) - df_nan.iloc[-1, 0] - 1), movie_id)
    movie_np = np.append(movie_np, last_record)

    data = data[pd.notnull(data[ratings])]
    data['movie_id'] = movie_np.astype(int)
    data[user_id] = data[user_id].astype(int)

    f = ['count','mean']

    df_movie_summary = data.groupby('movie_id')['rating'].agg(f)
    df_movie_summary.index = df_movie_summary.index.map(int)
    movie_benchmark = round(df_movie_summary['count'].quantile(0.7),0)
    drop_movie_list = df_movie_summary[df_movie_summary['count'] < movie_benchmark].index

    df_cust_summary = data.groupby('user_id')['rating'].agg(f)
    df_cust_summary.index = df_cust_summary.index.map(int)
    cust_benchmark = round(df_cust_summary['count'].quantile(0.7),0)
    drop_cust_list = df_cust_summary[df_cust_summary['count'] < cust_benchmark].index

    data = data[~data['movie_id'].isin(drop_movie_list)]
    data = data[~data['user_id'].isin(drop_cust_list)]

    return data

def get_best_movie_index(df):
    return df.groupby('movie_id')['ratings'].agg(['mean'])['mean'].idxmax()

def get_movies_summaries(data=None, with_titles=True, folder='data', filename='movie_titles.csv', col_names=['movie_id', 'date', 'title']):
    if data is not None and not with_titles:
        return data.groupby('movie_id')['rating'].agg(['mean','count'])
    elif data is None and with_titles:
        return pd.read_csv(
            os.path.join(folder, filename), header=None, names=col_names, encoding="ISO-8859-1"
        ).set_index('movie_id')
    elif data is not None and with_titles:
        return data.groupby('movie_id')['rating'] \
            .agg(['mean','count']) \
            .merge(
                pd.read_csv(
                    os.path.join(folder, filename), header=None, names=col_names, encoding="ISO-8859-1"
                    ).set_index('movie_id'),
                on='movie_id'
            )
    raise Exception("'data' must be set or 'with_titles' must be True!")

if __name__ == '__main__':
    df = load_data(num_files=1)
    print("Shape of df: ", df.shape)
    print(df.info())
    print(df.describe())
    print(df.head())