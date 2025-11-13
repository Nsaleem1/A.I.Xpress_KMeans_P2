#Testing different initialization points
#Note: change outer loop range in functions.py to 1 before running this test

import functions
import random
import statistics

locations = []
fileName = input("Enter name of file: ")

with open(fileName, "r") as text:
    distanceArr = {}
    for line in text:
        #split the x and y value and map them from string to float
        x, y = map(float, line.split())
        locations.append([x,y])

k = 3 #Value of k to test
numRuns = 50 #run kMeans algorithm "numRuns" time

results = []
print(f"========Testing input variability for K = {k} with {numRuns} runs=======")
for i in range(numRuns):
    random.seed(i) #different initial location each run
    clusters, distances = functions.kMeans(locations, k)
    totalDistance = sum(distances)
    results.append(totalDistance)
    print(f"Run {i+1}: Total distance= {round(totalDistance)}")

avg = sum(results) / len(results) #avg distance
best = min(results) #shortest distance
worst = max(results) #longest distance
stdev = statistics.stdev(results) #standard deviation

print(f"==============Results Summary=================")
print(f"Best distance: {round(best)}")
print((f"Worst Distance: {round(worst)}"))
print(f"Average Distance: {round(avg)}")
print(f"Standard Deviation: {round(stdev)}")