import math
import matplotlib.pyplot as plt
import random
import copy
import os

def euclideanDistance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

def output(k, clusters, distances):
    print(f"{k}) If you use {k} drone(s), the total route will be {int(sum(distances))} meters\n")
    for i in range(1,k + 1):
        print(f"\t{i}.\tLanding Pad {i} should be at {int(clusters[i - 1]['center'][0]), int(clusters[i-1]['center'][1])}, serving {len(clusters[i-1]['points'])} locations, route is {int(distances[i - 1])} meters\n")

# returns the list allClusterDistances, NN on each cluster -- the total distance for that
def nearestNeighbor(clusters):

    allClusterDistances = []
    allClusterRoutes = []

    for i in range(len(clusters)):
        clusterLoc = clusters[i]['points']

        #making sure list is not empty 
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
    max = 300

    for _ in range(50):

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

def plot_chosen_clusters(choice, clusters_list, filename):
    """
    Plots the chosen number of clusters as a JPEG.
    
    :param choice: int, number of clusters selected by the user
    :param clusters_list: list of cluster dictionaries [cluster0, cluster1, ...]
    :param filename: str, output filename
    """
    colors = ['orange', 'magenta', 'cyan', 'pink']

    # Only use the first 'choice' clusters
    clusters_to_plot = clusters_list[:choice]

    plt.figure(figsize=(8, 8))

    for i, cluster in enumerate(clusters_to_plot):
        color = colors[i % len(colors)]
        cluster_points = cluster['points']
        x_coords = [p[0] for p in cluster_points]
        y_coords = [p[1] for p in cluster_points]

        # Plot cluster points with unique color
        plt.scatter(
            x_coords, y_coords, s=20, 
            color=colors[i % len(colors)], alpha=0.6, label=f'Cluster {i+1}'
        )

        if 'route' in cluster and len(cluster['route']) > 1:
            route_x = [p[0] for p in cluster['route']]
            route_y = [p[1] for p in cluster['route']]
            plt.plot(route_x, route_y, color=color, linewidth=1.2, alpha=0.8)

        # Plot cluster center / landing pad as BIG distinct dot
        plt.scatter(
            cluster['center'][0], cluster['center'][1], s=250,  # bigger than points
            color=colors[i % len(colors)], edgecolor='black', marker='X', label=f'Center {i+1}'
        )

    plt.title(f"K-Means Clusters ({choice} Clusters)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)

    # Save as JPEG
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    image_path = os.path.join(desktop, f"{filename}_SOLUTION_{choice}.jpeg")
    #file_path = os.path.join(desktop, f"{filename}_{choice}_SOLUTION_FIX_DIST.txt")
    
    # plt.savefig(image_path, dpi=300)
    plt.axis('equal')
    plt.savefig(image_path, format='jpeg')
    plt.close()
    print(f"Clusters plotted and saved as {filename}_OVERALL_SOLUTION_{choice}.jpeg\n")


def cluster_dict_to_list(cluster_dict):
    return [cluster_dict[i] for i in range(len(cluster_dict))]

def save_cluster_locations(clusters, locations, distances, filename):
    """
    Saves each cluster's location numbers (1-based indices) to a separate text file.
    Each file name includes the total route distance for that cluster.

    :param clusters: list of cluster dictionaries [{center: (), points: []}, ...]
    :param locations: list of all original (x, y) points in order
    :param distances: list of total route distances for each cluster
    :param filename: base filename for output files
    """
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")

    for i, cluster in enumerate(clusters, start=1):
        cluster_points = cluster['points']
        cluster_indices = []

        # Get the location numbers (1-based)
        for p in cluster_points:
            if p in locations:
                cluster_indices.append(locations.index(p) + 1)

        # Include distance in filename (rounded to integer meters)
        cluster_distance = int(distances[i - 1]) if i - 1 < len(distances) else 0
        cluster_file_path = os.path.join(
            desktop,
            f"{filename}_{i}_SOLUTION_{cluster_distance}.txt"
        )

        # Write to file
        with open(cluster_file_path, 'w') as f:
            f.write(f"Landing Pad Center: {cluster['center']}\n")
            f.write(f"Total Route Distance: {cluster_distance} meters\n")
            f.write(f"Number of Locations: {len(cluster_indices)}\n\n")
            f.write("Locations in this cluster:\n")
            for loc_num in cluster_indices:
                f.write(f"{loc_num}\n")

        print(f"{filename}_{i}_SOLUTION_{cluster_distance}.txt saved to desktop")
   
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



            






