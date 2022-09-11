#!/usr/bin/python3


import sys
from itertools import permutations


for line in sys.stdin:
    line = line.strip()
    user_id, rating_list = line.split('\t', 1)
    user_mean_rating = 0.0
    films_counter = 0
    films_list = rating_list.split(',')
    for rating in films_list:
        films_counter += 1
        user_mean_rating += float(rating.split(' ')[1])
    user_mean_rating /= films_counter
    for pair in permutations(films_list, 2):
        film_id1, rating1 = pair[0].split(' ')
        film_id2, rating2 = pair[1].split(' ')
        print(film_id1 + ' ' + film_id2 + '\t' + user_id + ',' + str(user_mean_rating) + ',' + rating1 + ',' + rating2)
