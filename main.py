
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
print(f"There are {len(locations)} nodes: Solutions will be available by {pst_time.strftime("%-I:%M %p")}\n")


# these store center: (x,y) AND points = [] 
cluster1 = {}
cluster2 = {}
cluster3 = {}
cluster4 = {}

cluster1, dist = functions.kMeans(locations, 1)
functions.output(1, cluster1, dist)
cluster2, dist = functions.kMeans(locations, 2)
functions.output(2,cluster2, dist)
cluster3, dist = functions.kMeans(locations, 3)
functions.output(3, cluster3, dist)
cluster4, dist = functions.kMeans(locations, 4)
functions.output(4, cluster4, dist)


choice = input("Please select your choice 1 to 4: ")

#run nearest neighbor again, but this time save the files and make plots 
              









