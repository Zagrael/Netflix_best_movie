import numpy as np
from group_users import mean_notes, match

users_id = [10, 24, 36, 50, 15]
user_notes = [[4,2,3,0,4],[0,0,3,5,4],[1,5,3,1,1],[4,0,3,5,4],[0,5,5,5,0]]
nb_films = 5
nb_users = 4
groups = [[2,3],[0,1,4]]
group_notes = []
match_result = np.array([])
eps = 0.1

#result = match(user_notes[0], user_notes[3])
#print (result)