import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from data import load_data, get_movies_summaries

### Which film to rate ?
def ETC(ratings, m, user_ids, movie_ids):
    n_users, n_movies = ratings.shape

    # Data shuffling
    u_perm = np.random.permutation(n_users)
    m_perm = np.random.permutation(n_movies)
    ratings = ratings[u_perm,:]
    ratings = ratings[:,m_perm]
    user_ids = user_ids[u_perm]
    movie_ids = movie_ids[m_perm]
    # print('movies')
    # print(movie_ids)

    users_experience = [[] for _ in range(n_users)] # Movies each user has viewed
    sums = np.zeros((n_movies,), dtype=int) # Ratings'sum of each movie
    counts = np.zeros((n_movies,), dtype=int) # Ratings'count of each movie
    eligible = [True for _ in range(n_movies)]

    for i in range(m):
        k = 0
        for j in range(n_movies):
            if not eligible[j]:
                continue
            eligible[j] = False
            for l in np.append(np.arange(k,n_users), np.arange(0,k)):
                if ratings[l,j] and movie_ids[j] not in users_experience[l]:
                    sums[j] += ratings[l,j]
                    counts[j] += 1
                    users_experience[l].append(movie_ids[j])
                    eligible[j] = True
                    break
            k += 1
    # print('sums')
    # print(sums)
    # print('counts')
    # print(counts)
    # print('eligible')
    # print(eligible)
    means = np.where(eligible,sums/counts,np.zeros(sums.shape, dtype=int))
    # print('means')
    # print(means)
    return movie_ids[np.argmax(means)]

### Which user to ask ?

if __name__ == '__main__':
    # import sys
    # nb_files = 4
    # if len(sys.argv) > 1:
    #     nb_files = int(sys.argv[1])

    ratings = np.array([
        [4,2,3,0,4],
        [0,0,3,5,4],
        [1,5,3,1,1],
        [4,0,3,5,4]
    ])
    user_ids = np.array([1,2,3,4])
    movie_ids = np.array([152,589,147,253,214])
    # print('true_means')
    # print(np.mean(ratings, axis=0))

    m = 4
    best_movie = ETC(ratings, m, user_ids, movie_ids)

    # print(best_movie)

    # df = load_data(num_files=nb_files)
    # movies = load_movies(data=df)

    # true_means = movies.mean_rating.sort_index().to_numpy() # True mean ratings
    # num_movies = len(true_means)
    # num_users = len(df.user_id.unique())
    # ratings = np.empty((num_users, num_movies), dtype=int)