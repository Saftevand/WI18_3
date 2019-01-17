import json
from review import Review
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math

file = open("C:/Users/mathias/Desktop/Musical_Instruments_5.json", "r")

reviews = []

for i in file:
    x = json.loads(i)
    reviews.append(Review(x['reviewerID'], x['asin'], x['reviewText'], x['overall']))

def stringCleaner(input):
    input = input.lower()
    cleansed = input.replace(".", "")
    cleansed = cleansed.replace("!", "")
    cleansed = cleansed.replace("?", "")
    cleansed = cleansed.replace(";", "")
    cleansed = cleansed.replace(":", "")
    cleansed = cleansed.replace("  ", " ")
    return cleansed

allthewords = {}
allthewords["<PAD>"] = 0
allthewords["<START>"] = 1
allthewords["<UNK>"] = 2
allthewords["<UNUSED>"] = 3
idx = 4
for i in reviews:
    i.rText = stringCleaner(i.rText)
    for j in i.rText:
        if j not in allthewords:
            allthewords[j] = idx
            idx += 1

for i in reviews:
    for j in i.rText:
        i.rVector.append(allthewords[j])

train = reviews[0:math.floor(len(reviews)*0.8)]
test = reviews[math.floor(len(reviews)*0.8):]

k = 4

check_against = test[0]

def uniform_vectors(x : list, y : list):
    x_1 = []
    y_1 = []

    for i in x:
        x_1.append(i)
    for i in y:
        y_1.append(i)



    for i in x_1:
        if i not in y_1:
            y_1.append(0)

    for i in y_1:
        if i not in x_1:
            x_1.append(0)


    xx = len(x_1) - len(y_1)
    yy = len(y_1) - len(x_1)

    if xx > yy:
        for i in range(xx):
            y_1.append(0)
    else:
        for i in range(yy):
            x_1.append(0)

    return x_1, y_1

count = 0
for u in test[:10]:
    print(count)
    count += 1
    k_nearest = []
    for i in train:

        x, y = uniform_vectors(i.rVector, u.rVector)
        x = np.array(x).reshape(1, -1)
        y = np.array(y).reshape(1, -1)
        i.similarity = cosine_similarity(x, y)

        if (len(k_nearest) < k):
            k_nearest.append(i)
        else:
            temp = i
            remove = Review
            add = False
            for j in k_nearest:
                if (temp.similarity < j.similarity):
                    add = True
                    temp = j
                    remove = j
            if add:
                k_nearest.append(i)
                k_nearest.remove(remove)

    counter = [0, 0, 0, 0, 0]


    for i in k_nearest:
        if i.score == 1.0:
            counter[0] += 1
        if i.score == 2.0:
            counter[1] += 1
        if i.score == 3.0:
            counter[2] += 1
        if i.score == 4.0:
            counter[3] += 1
        if i.score == 5.0:
            counter[4] += 1

    u.predicted_score = np.argmax(np.array(counter)) + 1

for i in test[0:10]:
    print(i.predicted_score, i.score)