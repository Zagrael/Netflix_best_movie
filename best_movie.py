import pandas as pd
import numpy as np
from data import load_data, load_movies

### Which film to rate ?
def ETC(n_movies, m, ratings):
    if np.min(np.count_nonzero(ratings, axis=0)) < m:
        return np.argmin(ratings)
    return np.argmax(np.mean(ratings))

### Which user to ask ?

if __name__ == '__main__':
    import sys
    nb_files = 4
    if len(sys.argv[0]) > 1:
        nb_files = int(sys.argv[1])
    df = load_data(num_files=nb_files)
    movies = load_movies(data=df)

    true_means = movies.mean_rating.sort_index().to_numpy() # True mean ratings
    num_movies = len(true_means)
    num_users = len(df.user_id.unique())
    ratings = np.empty((num_users, num_movies), dtype=int)