import random
import math
import numpy as np

def randomColor():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def randomCentroid(data, max):
    number = random.randint(0, max)
    return data[number]

def euclideanDistance(c1, c2):
    if len(c1) == len(c2):
        sum = 0
        for i in  range(0,len(c1)):
            a = float(c1[i]) - float(c2[i])
            sum += a * a
        return round(math.sqrt(sum), 2)

def calculateCentroid(dataset):
    newPoint = []
    for i in  range(0,len(dataset)):
        for j in  range(0,len(dataset[i])):
            if j > len(newPoint)-1:
                newPoint.insert(j, float(dataset[i][j]))
            else:
                newPoint[j] = newPoint[j] + float(dataset[i][j])
    newCord = [];
    for k in  range(0,len(newPoint)):
        newCord.append(round(float(newPoint[k]) / len(dataset), 2))
    return newCord

def calculateWCSS(cluster):
    wcss = 0
    for property in cluster:
        center = calculateCentroid(cluster[property])
        for item in cluster[property]:
            distance = euclideanDistance(item, center)
            wcss += distance
    return round(wcss, 2)

def calculateTSS(data):
    tss = 0
    center = calculateCentroid(data)
    for item in data:
        distance = euclideanDistance(item, center)
        tss += distance
    return round(tss, 2)

def search(cluster, search_data):
    for property in cluster:
        for item in cluster[property]:
            if np.array_equal(item, search_data):
                return property