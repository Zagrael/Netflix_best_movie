import numpy as np
from groups_fct import match, mean_notes
from data import load_data

users_id = [10, 24, 36, 50, 15]
notes = [[4,2,3,0,4],[0,0,3,5,4],[1,5,3,1,1],[4,0,3,5,4],[0,5,5,5,0]]
film_notes = [[4,2,3,0,4],[0,0,3,5,4],[1,5,3,1,1],[4,0,3,5,4],[0,5,5,5,0]]
nb_films = 5
nb_users = 5
groups = []
group_notes = []
eps = 4

df = load_data()

for i, value in enumerate(users_id) :
    
    match_result = np.array([])
    
    if (i==0) :
        
        groups.append([i])
        group_notes.append(notes[i])
    
    else :
        
        print ("notes : ", notes[i])
        for j in range (len(groups)):
            ind, result = match(notes[i], group_notes[j])
            match_result = np.append(match_result,result)
            
        print("match user",i," : ", match_result)

        if (np.min(match_result) < eps) :
            print("min match : ", np.min(match_result))
            print("groups avant : ", groups)
            groups[match_result.argmin()].append(i)
            
            print("groups après : ", groups)
            group_notes[match_result.argmin()] = mean_notes(match_result.argmin(), nb_films, groups, notes)

        else :
            print("groups avant : ", groups)
            a = len(groups)
            groups.append([i])
            group_notes.append(notes[i])
            print("groups après : ", groups)
   
