#!/usr/bin/python3


import csv


ANSWER_FILE_NAME = 'part-00000'
FILMS_FILE_NAME = 'movies.csv'

answer_file = open(ANSWER_FILE_NAME, 'r')
films_file = csv.reader(open(FILMS_FILE_NAME, 'r'))
id_film_dict = dict()
next(films_file)
for line in films_file:
    id_film_dict[line[0]] = line[1]

answer_list = []

for line in answer_file:
    line = line.strip()
    user_id, recommended_films = line.split('\t', 1)
    recommended_films = recommended_films.split(',')
    answer_dict = dict()
    ratings_list = []
    for film_id, rating in map(lambda x: x.split(' '), recommended_films):
        rating = float(rating)
        if rating > 5.0:
            rating = 5.0
        if rating in answer_dict:
            answer_dict[rating].append(id_film_dict[film_id])
        else:
            ratings_list.append(rating)
            answer_dict[rating] = [id_film_dict[film_id]]

    answer_str = user_id
    for rating in sorted(ratings_list, reverse=True):
        for film_name in sorted(answer_dict[rating]):
            answer_str += '@' + str(rating) + '#' + film_name

    answer_list.append(answer_str)

for line in sorted(answer_list, key=lambda x: int(x.split('@', 1)[0])):
    print(line)
