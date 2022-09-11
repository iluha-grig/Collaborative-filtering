#!/usr/bin/python3


import sys


user_id = None
ratings = []
current_user_id = None

for line in sys.stdin:
    line = line.strip()
    user_id, film_rating = line.split('\t', 1)
    if current_user_id != user_id:
        if current_user_id:
            print(current_user_id + '\t' + ','.join(ratings))
            ratings = []
        current_user_id = user_id
    ratings.append(film_rating)

print(current_user_id + '\t' + ','.join(ratings))
