#!/usr/bin/python3


import sys


user_id = None
current_user_id = None
answer_dict = dict()

for line in sys.stdin:
    line = line.strip()
    user_id, films = line.split('\t', 1)
    if current_user_id != user_id:
        if current_user_id:
            prepare_list = []
            for film, predicted_rating in answer_dict.items():
                if predicted_rating[1] > 0.0:
                    prepare_list.append(film + ' ' + str(predicted_rating[0] / predicted_rating[1]))
            print(current_user_id + '\t' + ','.join(prepare_list))
            answer_dict = dict()
        current_user_id = user_id
    films = films.split(',')
    for film, similarity, rating in map(lambda z: z.split(' '), films):
        if film in answer_dict:
            x, y = answer_dict[film]
            answer_dict[film] = (x + float(similarity) * float(rating), y + float(similarity))
        else:
            answer_dict[film] = (float(similarity) * float(rating), float(similarity))

prepare_list = []
for film, predicted_rating in answer_dict.items():
    if predicted_rating[1] > 0.0:
        prepare_list.append(film + ' ' + str(predicted_rating[0] / predicted_rating[1]))
print(current_user_id + '\t' + ','.join(prepare_list))
