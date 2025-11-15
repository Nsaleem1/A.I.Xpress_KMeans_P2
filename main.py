import math
import random
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import functions

#reading the file and storing coordinates into locations array
locations = []
route_x = []
route_y = []
fileName = input("Enter name of file: ")

with open(fileName, "r") as text:
    for line in text:
        #split the x and y value and map them from string to float
        x, y = map(float, line.split())
        locations.append([x,y])
        #ensuring nodes do not exceed limit
        if len(locations) > 4096:
            raise Exception("Max amount of Nodes in file reached")
#time
pst_time = datetime.now(ZoneInfo("America/Los_Angeles")) + timedelta(minutes=5)
print(f"There are {len(locations)} nodes: Solutions will be available by {pst_time.strftime('%I:%M %p').lstrip('0')}\n")


# these store center: (x,y) AND points = [] 
cluster1 = {}
cluster2 = {}
cluster3 = {}
cluster4 = {}

cluster1, dist1 = functions.kMeans(locations, 1)
functions.output(1, cluster1, dist1)
sse1 = functions.totalSSE(cluster1)

cluster2, dist2 = functions.kMeans(locations, 2)
functions.output(2,cluster2, dist2)
sse2 = functions.totalSSE(cluster2)

cluster3, dist3 = functions.kMeans(locations, 3)
functions.output(3, cluster3, dist3)
sse3 = functions.totalSSE(cluster3)

cluster4, dist4 = functions.kMeans(locations, 4)
functions.output(4, cluster4, dist4)
sse4 = functions.totalSSE(cluster4)

with open("sseVals.txt", "w") as f:
    f.write(f"{fileName} for k = 1 sse is {sse1}\n")
    f.write(f"{fileName} for k = 2 sse is {sse2}\n")
    f.write(f"{fileName} for k = 3 sse is {sse3}\n")
    f.write(f"{fileName} for k = 4 sse is {sse4}\n")

choice = int(input("Please select your choice 1 to 4: "))
 
if (choice == 1):
    clustersList = functions.clusterDictToList(cluster1)
    correctDist = dist1
if (choice == 2):
    clustersList = functions.clusterDictToList(cluster2)
    correctDist = dist2
if (choice == 3):
    clustersList = functions.clusterDictToList(cluster3)
    correctDist = dist3
if (choice == 4):
    clustersList = functions.clusterDictToList(cluster4)
    correctDist = dist4
    
functions.plotChosenClusters(choice, clustersList, fileName)
functions.listClusterLocations(clustersList, locations, correctDist, fileName)