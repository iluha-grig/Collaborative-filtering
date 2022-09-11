#!/usr/bin/python3


import sys
import numpy as np


film_id1 = None
film_id2 = None
current_film_id1 = None
current_film_id2 = None
films_list = []
users_list = []
first_iter_flag = True
numerator = 0.0
denominator1 = 0.0
denominator2 = 0.0

for line in sys.stdin:
    line = line.strip()
    film_pair, value = line.split('\t', 1)
    film_id1, film_id2 = film_pair.split(' ')
    if first_iter_flag:
        first_iter_flag = False
        current_film_id1 = film_id1
        current_film_id2 = film_id2
    if current_film_id1 != film_id1:
        # print
        similarity = numerator / (np.sqrt(denominator1) * np.sqrt(denominator2))
        if similarity < 0.0:
            similarity = 0.0
        insert_string = current_film_id2 + ' ' + str(similarity) + ':' + ','.join(
            map(lambda x: x[0] + ' ' + x[1], users_list))
        films_list.append(insert_string)
        users_list = []
        numerator = 0.0
        denominator1 = 0.0
        denominator2 = 0.0
        current_film_id2 = film_id2
        print(current_film_id1 + '\t' + ';'.join(films_list))
        films_list = []
        current_film_id1 = film_id1
    elif current_film_id2 != film_id2:
        # add in films_list
        similarity = numerator / (np.sqrt(denominator1) * np.sqrt(denominator2))
        if similarity < 0.0:
            similarity = 0.0
        insert_string = current_film_id2 + ' ' + str(similarity) + ':' + ','.join(
            map(lambda x: x[0] + ' ' + x[1], users_list))
        films_list.append(insert_string)
        users_list = []
        numerator = 0.0
        denominator1 = 0.0
        denominator2 = 0.0
        current_film_id2 = film_id2
    user_id, user_mean_rating, rating1, rating2 = value.split(',')
    users_list.append((user_id, rating1))
    numerator += (float(rating1) - float(user_mean_rating)) * (float(rating2) - float(user_mean_rating))
    denominator1 += (float(rating1) - float(user_mean_rating)) ** 2
    denominator2 += (float(rating2) - float(user_mean_rating)) ** 2

similarity = numerator / (np.sqrt(denominator1) * np.sqrt(denominator2))
if similarity < 0.0:
    similarity = 0.0
insert_string = current_film_id2 + ' ' + str(similarity) + ':' + ','.join(map(lambda x: x[0] + ' ' + x[1], users_list))
films_list.append(insert_string)
print(current_film_id1 + '\t' + ';'.join(films_list))
