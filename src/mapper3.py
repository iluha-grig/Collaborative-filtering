#!/usr/bin/python3


import sys


for line in sys.stdin:
    line = line.strip()
    key, value = line.split('\t', 1)
    value = value.split(';')
    films_list = []
    for film_string in value:
        left_part, right_part = film_string.split(':')
        film_id, similarity = left_part.split(' ')
        right_part = right_part.split(',')
        users_dict = dict(map(lambda x: tuple(x.split(' ')), right_part))
        films_list.append((film_id, similarity, users_dict))

    answer_dict = dict()

    for counter, film in enumerate(films_list):
        for k, v in film[2].items():
            if k not in answer_dict:
                k_list = []
                for counter2, film2 in enumerate(films_list):
                    if counter2 < counter:
                        k_list.append((film2[0], film2[1], v))
                    elif k not in film2[2]:
                        k_list.append((film2[0], film2[1], v))
                if k_list:
                    answer_dict[k] = k_list
                else:
                    answer_dict[k] = None

    for user, unwatched_films in answer_dict.items():
        if unwatched_films is not None:
            print(user + '\t' + ','.join(map(lambda x: ' '.join(x), unwatched_films)))
