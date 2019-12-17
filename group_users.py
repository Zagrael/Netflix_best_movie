import numpy as np

users_id = [10, 24, 36, 50, 15]
user_notes = [[4,2,3,0,4],[0,0,3,5,4],[1,5,3,1,1],[4,0,3,5,4],[0,5,5,5,0]]
nb_films = 5
nb_users = 4
groups = []
group_notes = []
eps = 4

def match(V1, V2):
    compare = 0
    V1_rates_seen = np.array([])
    V2_rates_seen = np.array([])
    V1 = np.array(V1)
    V2 = np.array(V2)
    
    result = np.logical_and(V1,V2)
    
    for i in range(len(result)) :
        if (result[i] == True) :
            V1_rates_seen = np.append(V1_rates_seen, V1[i])
            V2_rates_seen = np.append(V2_rates_seen, V2[i])
            compare += 1
    
    dist = np.linalg.norm(V1_rates_seen-V2_rates_seen)        
    match_value = compare/len(result)
    return match_value, dist

def mean_notes(id_group):
    nb_films = 5
    sum = np.zeros(nb_films)
    div = 0

    for i in range (0,len(groups[id_group])) :
        # parcourt les id_users
        sum += user_notes[groups[id_group][i]] 
        div += 1
    
    mean = sum/div
    return mean

for i, value in enumerate(users_id) :
    
    match_result = np.array([])
    
    if (i==0) :
        
        groups.append([i])
        group_notes.append(user_notes[i])
    
    else :
        
        print ("user_notes : ", user_notes[i])
        for j in range (len(groups)):
            ind, result = match(user_notes[i], group_notes[j])
            match_result = np.append(match_result,result)
            
        print("match user",i," : ", match_result)

        if (np.min(match_result) < eps) :
            print("min match : ", np.min(match_result))
            print("groups avant : ", groups)
            groups[match_result.argmin()].append(i)
            
            print("groups après : ", groups)
            group_notes[match_result.argmin()] = mean_notes(match_result.argmin())

        else :
            print("groups avant : ", groups)
            a = len(groups)
            groups.append([i])
            group_notes.append(user_notes[i])
            print("groups après : ", groups)
   
