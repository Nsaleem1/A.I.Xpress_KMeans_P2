import math
import matplotlib.pyplot as plt
import random
import copy
import os

def euclideanDistance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

def output(k, clusters, distances):
    roundedDists = [round(d) for d in distances]
    total = sum(roundedDists)

    print(f"{k}) If you use {k} drone(s), the total route will be {total} meters\n")
    for i in range(1, k + 1):
        center = clusters[i - 1]['center']
        print(f"\t{i}.\tLanding Pad {i} should be at ({int(center[0])}, {int(center[1])}), serving {len(clusters[i-1]['points'])} locations, route is {roundedDists[i - 1]} meters\n")

# returns the list allClusterDistances, NN on each cluster -- the total distance for that
def nearestNeighbor(clusters):

    allClusterDistances = []
    allClusterRoutes = []

    for i in range(len(clusters)):
        clusterLoc = clusters[i]['points']

        # making sure list is not empty 
        if not clusterLoc:
            allClusterDistances.append(0)
            allClusterRoutes.append([])
            continue

        unvisited = list(range(len(clusterLoc)))  
        visited = []
        clusterDistance = 0
        current = -1  
        nextPoint = 0
        route = [clusters[i]['center']]

        # keep iterating until all nodes have been visited
        while len(unvisited) > 0:
            smallestDist = float('inf')

            # find nearest neighbor
            for j in unvisited:
                if current == -1:
                    # landing pad to the NN
                    dist = euclideanDistance(clusters[i]['center'], clusterLoc[j])
                else:
                    dist = euclideanDistance(clusterLoc[current],clusterLoc[j])
                                             
                if dist < smallestDist:
                    smallestDist = dist
                    nextPoint = j

            # update distance, arrays, and current node
            clusterDistance += smallestDist

            unvisited.remove(nextPoint)
            visited.append(nextPoint)
            current = nextPoint
            route.append(clusterLoc[current])

        # back to the landing pad (cluster center)
        clusterDistance += euclideanDistance(clusterLoc[current], clusters[i]['center'])

        allClusterDistances.append(clusterDistance)
        allClusterRoutes.append(route)

    return allClusterDistances, allClusterRoutes

# returns BSFclusters and BSFallDistances
# BSFclusters = {center: (x,y) points: [] } for each cluster
# BSFallDistances = [dist1, dist2] the NN total distance route of each cluster 

def kMeans(locations, k):
    clusters = {}
    BSFclusters = {}
    BSFtotalDistance = float('inf')
    BSFallDistances = []
    movement = 0.1
    max = 100

    for _ in range(25):

        #choosing random locations for the center
        for i in range(k):
            randCenters = random.sample(locations, k)
            clusters[i] = { 'center' : randCenters[i], 'points' : [] }
    
        #assign points and move center, repeat until movement is limited or reach max 
        for iteration in range (max):

            #empty points 
            for i in range(k):
                clusters[i]['points'] = []
            
            #reassign points
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
                if len(points) == 0:
                    clusters[i]['center'] = random.choice(locations)
                    continue
                avgX = sum(p[0] for p in points) / len(points)
                avgY = sum(p[1] for p in points) / len(points)
                newCenter = (avgX, avgY)
                if euclideanDistance(newCenter, clusters[i]['center']) > movement:
                    centersMoved = True
                clusters[i]['center'] = newCenter
            
            allClusterDistances, allClusterRoutes = nearestNeighbor(clusters)
            totalDistance = sum(allClusterDistances)

            if totalDistance < BSFtotalDistance:
                BSFtotalDistance = totalDistance
                for i, route in enumerate(allClusterRoutes):
                    clusters[i]['route'] = route
                BSFclusters = copy.deepcopy(clusters)
                BSFallDistances = copy.deepcopy(allClusterDistances)
            
            #if the centers are not moving, break out of the iteration loop
            if not centersMoved:
                break
    
    return BSFclusters, BSFallDistances

def plotChosenClusters(choice, clustersList, filename):
    
    colors = ['orange', 'magenta', 'cyan', 'pink']

    # Only use the choice clusters
    clustersToPlot = clustersList[:choice]

    plt.figure(figsize=(15, 15))

    for i, cluster in enumerate(clustersToPlot):
        color = colors[i % len(colors)]
        clusterPoints = cluster['points']
        x_coords = [p[0] for p in clusterPoints]
        y_coords = [p[1] for p in clusterPoints]

        plt.scatter(
            x_coords, y_coords, s=20, 
            color=colors[i % len(colors)], alpha=0.6, label=f'Cluster {i+1}'
        )

        if 'route' in cluster and len(cluster['route']) > 1:
            fullRoute = [cluster['center']] + cluster['route'] + [cluster['center']]
            route_x = [p[0] for p in fullRoute]
            route_y = [p[1] for p in fullRoute]
            plt.plot(route_x, route_y, color=color, linewidth=1.2, alpha=0.8)

        # landing pad is big X
        plt.scatter(
            cluster['center'][0], cluster['center'][1], s=250,  
            color=colors[i % len(colors)], edgecolor='black', marker='X', label=f'Center {i+1}'
        )

    plt.title(f"K-Means ({choice} Cluster(s)) on {filename}", fontsize=32)
    plt.xlabel("X Coordinate Values", fontsize=24)
    plt.ylabel("Y Coordinate Values", fontsize=24)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.grid(True)

    # Save as JPEG
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    imagePath = os.path.join(desktop, f"{filename[:-4]}_OVERALL_SOLUTION.jpeg")
    
    plt.axis('equal')
    plt.savefig(imagePath, format='jpeg')
    plt.close()
    print(f"Image of clusters saved to desktop as {filename[:-4]}_OVERALL_SOLUTION.jpeg\n")

def clusterDictToList(clusterDict):
    return [clusterDict[i] for i in range(len(clusterDict))]

def listClusterLocations(clusters, locations, distances, filename):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")

    for i, cluster in enumerate(clusters, start=1):
        clusterPoints = cluster['points']
        clusterIndices = []

        # Get the location numbers 
        for p in clusterPoints:
            if p in locations:
                clusterIndices.append(locations.index(p) + 1)

        # Include distance in filename 
        clusterDistance = round(distances[i - 1]) if i - 1 < len(distances) else 0
        clusterFilePath = os.path.join(
            desktop,
            f"{filename[:-4]}_{i}_SOLUTION_{clusterDistance}.txt"
        )

        # Write to file
        with open(clusterFilePath, 'w') as f:
            for locNum in clusterIndices:
                f.write(f"{locNum}\n")

        print(f"{filename[:-4]}_{i}_SOLUTION_{clusterDistance}.txt saved to desktop")
   
def SSE(center, points):
    cx, cy = center
    sse = 0
    for x, y in points:
        dx = x - cx
        dy = y - cy
        sse += dx*dx + dy*dy
    return sse

def totalSSE(clusters):
    total = 0
    for clusterData in clusters.values():
        center = clusterData["center"]
        points = clusterData["points"]
        total += SSE(center, points)  # SSE computes sum of squared distances for this cluster
    return total



            






