from Movielens_classes import user, movie
import numpy as np

file_subset1_train = open("C:/Users/mathias/Desktop/ml-100k/subset_train.txt", "r")
file_subset1_test = open("C:/Users/mathias/Desktop/ml-100k/subset_test.txt", "r")
file_subset1_training = file_subset1_train.readlines()
file_subset1_testing = file_subset1_test.readlines()


all_movies_average = 0
users = []
movies = []
ratings_accum = 0
add = True
s = 0

for i in file_subset1_training:
    splitted = i.split('\t')
    for j in users:
        if j.ID == int(splitted[0]):
            add = False
    if add:
        users.append(user(int(splitted[0])))
    add = True
    for j in movies:
        if j.ID == int(splitted[1]):
            add = False
    if add:
        movies.append(movie(int(splitted[1])))
    add = True
    ratings_accum += int(splitted[2])
    users[int(splitted[0])-1].rating_accum += int(splitted[2])
    for j in movies:
        if j.ID == int(splitted[1]):
            j.rating_accum += int(splitted[2])
            j.times_reviewed += 1
            users[int(splitted[0]) - 1].movies_reviewed.append(j)

all_movies_average = ratings_accum / len(file_subset1_training)
for i in users:
    i.bias = (i.rating_accum / len(i.movies_reviewed)) - all_movies_average
for i in movies:
    i.bias = (i.rating_accum / i.times_reviewed) - all_movies_average


r_ui = np.zeros((len(users), len(movies)))
pred_r_ui = np.zeros((len(users), len(movies)))
b_ui = np.zeros((len(users), len(movies)))

for i in range(len(b_ui)):
    for j in range(len(b_ui[i])):
        b_ui[i][j] = all_movies_average + users[i].bias + movies[j].bias

for i in range(len(pred_r_ui)):
    for j in range(len(pred_r_ui[i])):
        pred_r_ui[i][j] = b_ui[i][j] + r_ui[i][j]

#Mangler at lave vectorne til users of movies, og så ud fra dem lave r_ui