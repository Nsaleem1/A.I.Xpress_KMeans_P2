import math
import matplotlib.pyplot as plt
import random
import copy

def euclideanDistance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

def output(k, clusters, distances):
    print(f"{k}) If you use {k} drone(s), the total route will be {int(sum(distances))} meters\n")
    for i in range(1,k + 1):
        print(f"\t{i}.\tLanding Pad {i} should be at {int(clusters[i - 1]['center'][0]), int(clusters[i-1]['center'][1])}, serving AHH locations, route is {int(distances[i - 1])} meters\n")

# returns the list allClusterDistances, NN on each cluster -- the total distance for that
def nearestNeighbor(clusters, locations, distanceMatrix):

    allClusterDistances = []

    for i in range(len(clusters)):
        clusterLoc = clusters[i]['points']
        #making sure list is not empty 
        if not clusterLoc:
            allClusterDistances.append(0)
            continue

         # Map cluster points to their indices in the original locations array
        clusterLocIndices = [locations.index(pt) for pt in clusterLoc]   

        unvisited = list(range(len(clusterLoc)))  
        visited = []
        clusterDistance = 0
        current = -1  
        nextPoint = 0

        # keep iterating until all nodes have been visited
        while len(unvisited) > 0:
            smallestDist = float('inf')

            # find nearest neighbor
            for j in unvisited:
                if current == -1:
                    # landing pad to random point 
                    dist = euclideanDistance(clusters[i]['center'], clusterLoc[j])
                else:
                    # the indices in the cluster are not the same points from the distance matrix
                    matrixCurrent = clusterLocIndices[current]
                    matrixNext = clusterLocIndices[j]
                    dist = distanceMatrix[matrixCurrent][matrixNext]

                if dist < smallestDist:
                    smallestDist = dist
                    nextPoint = j

            # update distance, arrays, and current node
            clusterDistance += smallestDist

            unvisited.remove(nextPoint)
            visited.append(nextPoint)
            current = nextPoint

        # back to the landing pad (cluster center)
        clusterDistance += euclideanDistance(clusterLoc[current], clusters[i]['center'])

        allClusterDistances.append(clusterDistance)

    return allClusterDistances

# returns BSFclusters and BSFallDistances
# BSFclusters = {center: (x,y) points: [] } for each cluster
# BSFallDistances = [dist1, dist2] the NN total distance route of each cluster 

def kMeans(locations, k, distanceMatrix):
    clusters = {}
    BSFclusters = {}
    BSFtotalDistance = float('inf')
    BSFallDistances = []
    movement = 1e-4
    max = 100

    for _ in range(10):

        #choosing random location for center 
        for i in range(k):
            randCenters = random.sample(locations, k)
            clusters[i] = { 'center' : randCenters[i], 'points' : [] }
        
        #assigning cluster points
        for iteration in range (max):
            for i in range(k):
                clusters[i]['points'] = []
            
            for loc in locations:
                shortestDist = float('inf')
                closestCluster = None
                for j in range(k):
                    dis = euclideanDistance(clusters[j]['center'], loc)
                    if dis < shortestDist:
                        shortestDist = dis
                        closestCluster = j
                clusters[closestCluster]['points'].append(loc)
        
            #updating center
            centersMoved = False
            for i in range(k):
                points = clusters[i]['points']
                avgX = sum(p[0] for p in points) / len(points)
                avgY = sum(p[1] for p in points) / len(points)
                newCenter = (avgX, avgY)
                if euclideanDistance(newCenter, clusters[i]['center']) > movement:
                    centersMoved = True
                clusters[i]['center'] = newCenter
            
            if not centersMoved:
                break
            
            allClusterDistances = nearestNeighbor(clusters, locations, distanceMatrix)
            totalDistance = sum(allClusterDistances)

            if totalDistance < BSFtotalDistance:
                BSFtotalDistance = totalDistance
                BSFclusters = copy.deepcopy(clusters)
                BSFallDistances = copy.deepcopy(allClusterDistances)
    
    return BSFclusters, BSFallDistances






        


            






