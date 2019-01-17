import json
from reviewer import Reviewer
from item import Item
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math
from operator import itemgetter
from scipy import spatial

file = open("C:/Users/marku/Desktop/Musical_Instruments_5.json", "r")

reviewers = []
reviewerNames = []

for i in file:
    x = json.loads(i)
    if x['reviewerID'] not in reviewerNames:
        reviewers.append(Reviewer(x['reviewerID']))
        reviewerNames.append(x['reviewerID'])
        reviewers[len(reviewerNames)-1].pIDs.append(x['asin'])
        reviewers[len(reviewerNames)-1].reviews.append(x['reviewText'])
        reviewers[len(reviewerNames)-1].scores.append(x['overall'])
    else:
        index = reviewerNames.index(x['reviewerID'])
        reviewers[index].pIDs.append(x['asin'])
        reviewers[index].reviews.append(x['reviewText'])
        reviewers[index].scores.append(x['overall'])

items = []
itemNames = []

file = open("C:/Users/marku/Desktop/Musical_Instruments_5.json", "r")
for u in file:
    x = json.loads(u)
    if x['asin'] not in itemNames:
        items.append(Item(x['asin']))
        itemNames.append(x['asin'])
        items[len(itemNames)-1].reviews.append(x['reviewText'])
        items[len(itemNames)-1].scores.append(x['overall'])
        items[len(itemNames)-1].reviewers.append(x['reviewerID'])

    else:
        index = itemNames.index(x['asin'])
        items[index].reviews.append(x['reviewText'])
        items[index].scores.append(x['overall'])
        items[index].reviewers.append(x['reviewerID'])


def stringCleaner(input):
    input = input.lower()
    cleansed = input.replace(".", "")
    cleansed = cleansed.replace("!", "")
    cleansed = cleansed.replace("?", "")
    cleansed = cleansed.replace(";", "")
    cleansed = cleansed.replace(":", "")
    cleansed = cleansed.replace(",", "")
    cleansed = cleansed.replace("  ", " ")
    return cleansed

allthewords = {}
allthewords["<PAD>"] = 0
allthewords["<START>"] = 1
allthewords["<UNK>"] = 2
allthewords["<UNUSED>"] = 3
idx = 4

for i in reviewers:
    counter = 0
    for u in i.reviews:
        u = stringCleaner(u)
        del i.reviews[counter:counter+1]
        i.reviews.insert(counter, u)
        u = u.split(' ')
        counter += 1
        for j in u:
            if j not in allthewords.keys():
                allthewords[j] = idx
                idx += 1

for i in reviewers:
    for j in i.reviews:
        temp = []
        a = j.split(' ')
        for k in a:
            temp.append(allthewords[k])
        i.rVectors.append(temp)

for i in items:
    counter = 0
    for u in i.reviews:
        u = stringCleaner(u)
        del i.reviews[counter:counter+1]
        i.reviews.insert(counter,u)
        counter += 1

for i in items:
    for j in i.reviews:
        temp = []
        a = j.split(' ')
        for k in a:
            temp.append(allthewords[k])
        i.rVectors.append(temp)

train = reviewers[0:math.floor(len(reviewers) * 0.8)]
test = reviewers[math.floor(len(reviewers) * 0.8):]



def uniform_vectors(x : list, y : list):
    x_1 = []
    y_1 = []

    for i in x:
        x_1.append(i)
    for i in y:
        y_1.append(i)

    xx = 0
    yy = 0


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


k = 4
user = reviewers[23]
recommendedItems = []

for i in items:
    similarities = []
    k_nearest = []
    if user.rID not in i.reviewers:
        for r in user.rVectors:

            for iV in i.rVectors:
                x, y = uniform_vectors(r, iV)
                x = np.array(x).reshape(1, -1)
                y = np.array(y).reshape(1, -1)
                similarities.append([user,r,i,cosine_similarity(x, y)])

    similarities = sorted(similarities, key=itemgetter(3))
    similarities.reverse()

    k_nearest = similarities[:k]
    counter = [0, 0, 0, 0, 0]

    for j in k_nearest:
        if j[0].scores[j[0].rVectors.index(j[1])] == 1.0:
            counter[0] += 1
        if j[0].scores[j[0].rVectors.index(j[1])] == 2.0:
            counter[1] += 1
        if j[0].scores[j[0].rVectors.index(j[1])] == 3.0:
            counter[2] += 1
        if j[0].scores[j[0].rVectors.index(j[1])] == 4.0:
            counter[3] += 1
        if j[0].scores[j[0].rVectors.index(j[1])] == 5.0:
            counter[4] += 1

    if np.argmax(np.array(counter)) + 1 > 3:
        recommendedItems.append(i)

for i in recommendedItems:
    print(i.pID)

print(len(recommendedItems))