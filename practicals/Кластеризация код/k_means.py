# Чтение данных из файла
def read_data(filename, encoding="utf-8-sig"):
    data=[]
    f = open(filename, encoding=encoding)
    for line in f:
        l = line.strip("\n").split("\t")
        for i in range(len(l)):
            l[i] = float(l[i])
        data.append(tuple(l))
    return tuple(data)

import random

def init_clusters_coordinates(data, count_clusters):
    if len(data) <= count_clusters:
        raise IndexError(data, count_clusters)
    data = list(data)
    output = []
    for _ in range(count_clusters):
        a = random.choice(data)
        data.remove(a)
        output.append(a)
    return tuple(output)

import math

def distance_of_points(p1, p2):
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

# Находит ближайшую точку к начальной.
# point: tuple of float.
# points: tuple of (tuple of float)
def find_near_point(point, points):
    min_id = None
    min_distance = None
    for i in range(len(points)):
        d = distance_of_points(point, points[i]) # 4
        if min_id == None or d < min_distance:
            min_distance = d
            min_id = i
    return min_id

from collections import defaultdict

def distribute_data_to_clusters(data, clusters_coordinates):
    output = defaultdict(list)
    for d in data:
        output[find_near_point(d, clusters_coordinates)].append(d)
    return output

def get_centroid(points):
    output = [0.0] * len(points[0])
    for p in points:
        for i in range(len(p)):
            output[i] += p[i]
    for i in range(len(output)):
        output[i] /= len(points)
    return tuple(output)

def get_centroids(clusters):
    output = [None] * len(clusters)
    for k, v in clusters.items():
        output[k] = get_centroid(v)
    return tuple(output)

def search_error(clusters, clusters_coordinates):
    output = 0.0
    for cluster_id, cluster_points in clusters.items():
        for point in cluster_points:
            for p, m in zip(point, clusters_coordinates[cluster_id]):
                output += (p - m) ** 2
    return output / len(clusters_coordinates)

def k_means(data, count_clusters, error = 0.1): # 1
    clusters_coordinates = init_clusters_coordinates(data, count_clusters) # 2
    e_history = set()
    while True:
        clusters = distribute_data_to_clusters(data, clusters_coordinates) # 3
        clusters_coordinates = get_centroids(clusters)
        e = search_error(clusters, clusters_coordinates)
        print(e)
        if e < error or e in e_history: break
        e_history.add(e)
    output = {}
    for k, v in clusters.items():
        output[clusters_coordinates[k]] = tuple(v)
    return output

def input_or_skip(msg, default = None):
    try:
        return float(input(msg))
    except:
        return default
    
print("cluster coordinate: list of points.")
for cluster, points in k_means(read_data(input("filename: ")), int(input("count clusters: ")), input_or_skip("error (or press enter to 0.1): ", 0.1)).items():
    print("{}:\n{}\n".format(cluster, points))
