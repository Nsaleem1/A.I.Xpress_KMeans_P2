#Testing larger values of K (K > 4)

import functions
locations = []
fileName = input("Enter name of file: ")

with open(fileName, "r") as text:
    distanceArr = {}
    for line in text:
        #split the x and y value and map them from string to float
        x, y = map(float, line.split())
        locations.append([x,y])

def k_values_test(locations):
    for k in range(5,9):
        clusters, distances = functions.kMeans(locations, k)
        totalDistance = sum(distances)
        print(f"Total distance = {round(totalDistance)} for K = {k}")

k_values_test(locations)

