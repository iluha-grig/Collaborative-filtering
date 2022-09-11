#!/usr/bin/python3


import sys


for line in sys.stdin:
    line = line.strip()
    user_id, predicted_ratings = line.split('\t', 1)
    predicted_ratings = predicted_ratings.split(',')
    for i in range(len(predicted_ratings)):
        pair = predicted_ratings[i].split(' ')
        pair[1] = float(pair[1])
        predicted_ratings[i] = tuple(pair)
    predicted_ratings = sorted(predicted_ratings, key=lambda x: x[1], reverse=True)
    predicted_ratings = predicted_ratings[:100]
    print(user_id + '\t' + ','.join(map(lambda x: x[0] + ' ' + str(x[1]), predicted_ratings)))
