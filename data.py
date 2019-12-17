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

    return data

if __name__ == '__main__':
    df = load_data(num_files=1)
    print("Shape of df: ", df.shape)
    print(df.info())
    print(df.describe())
    print(df.head())