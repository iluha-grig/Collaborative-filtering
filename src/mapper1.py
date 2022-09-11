#!/usr/bin/python3


import sys


for line in sys.stdin:
    line = line.strip()
    user_id, film_id, rating, timestamp = line.split(',')
    if user_id != 'userId':
        print('%s\t%s %s' % (user_id, film_id, rating))
