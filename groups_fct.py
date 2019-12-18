import numpy as np

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

def mean_notes(id_group, nb_films, groups, notes):
    sum = np.zeros(nb_films)
    div = 0

    for i in range (0,len(groups[id_group])) :
        # parcourt les id_users
        sum += notes[groups[id_group][i]] 
        div += 1
    
    mean = sum/div
    return mean