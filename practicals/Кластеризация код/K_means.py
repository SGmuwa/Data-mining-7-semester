import numpy as np
import pandas as pd
number_of_clusters = 4
# Чтение данных из файла
clustered_elements=[]
f = open("data_for_k_means.csv", encoding="utf-8-sig")
for line in f:
    l = line.strip("\n").split("\t")
    for i in range(len(l)):
        l[i] = float(l[i])
    clustered_elements.append(l)
data = np.array(clustered_elements)
print("Данные", data)


data.mean(axis = 0)
data.std(axis = 0)


def get_euclidean_distance (l1,l2):
    euclid = 0
    count = len(l1)
    for i in range(count):
        euclid += (l1[i]-l2[i])**2
    return euclid ** 0.5

list_for_serch_start_centers = []

# Центроид для всех данных:
centroid = (data.sum(axis = 0)) / data.shape[0]
print("Центроид", centroid)

#Ищем расстояние каждого элемента до центра:
for i in range(len(data)):
    r = get_euclidean_distance((data[i,:]).tolist(),centroid)
    list_for_serch_start_centers.append((i,r))
sort_lfssc = sorted(list_for_serch_start_centers, key=lambda el: el[1])
sort_lfssc.reverse()
print(sort_lfssc)

ind_centers = []
for i in range(number_of_clusters):
    el = sort_lfssc[i]
    ind_centers.append(el[0])
print(ind_centers)


# Алгоритм К-средних
import random
ind_centers = random.sample(list(range(data.shape[0])), number_of_clusters)
cluster_numbers = list(range(number_of_clusters))#Номера кластеров
print("ind_centers", ind_centers)
centers = []
for i in ind_centers:
    centers.append((data[i,:]).tolist())
list_index_cl = []
list_index_last = []



def get_cluster(l,cluster_numbers):
    global list_index_cl
    list_index_cl = []
    for n in cluster_numbers:
        list_index_cl.append([n,[]])
    for i in range(len(l)):
        cl_num = np.argmin(l[i])
        list_index_cl[cl_num][1].append(i)
        l[i].append(cl_num)
    print("Центр и индексы его элементов:",list_index_cl,"\n")
    return l

def get_error(l_distance):
    err = 0
    for it in l_distance:
        ind_min = it[number_of_clusters]
        err += it[ind_min]**2
    return err

def stop_criterion(l1,l2):
    return (np.array(l1)==np.array(l2)).all()


err_last = 1000
#Растояния каждого объекта от          (матрица для нахождения близжайшего центра для каждого объекта: l_distance)
#1 центра  2 центра  3 центра  4 центра
while True:
    l_distance = []
    print("Координаты центров: ",centers)
    for ob in data: #цикл по строкам
        l_centers = []
        for c in centers:
            l_centers.append(get_euclidean_distance(ob,c))
        l_distance.append(l_centers)

    l_distance = get_cluster(l_distance,cluster_numbers)
    err = get_error(l_distance)
    
    for ind_el in range(len(l_distance)):
        print(ind_el,l_distance[ind_el])
    print(err)

#     if abs(err-err_last)<0.0015: break
#     err_last = err

    
    #для каждого кластера вычисляется новый центроид и в него перемещается центр кластера
    l_centroid = []
    for el in list_index_cl:#для каждого кластера считается новый центр
        m = el[1]
        num_center_of_cl = data.shape[1] #число координат центра
        center_of_cl = []
        for i in range(num_center_of_cl):#Для каждок координаты центра
            temp_coord = 0 
            for j in m:
                temp_coord+=data[j,i]
            temp_coord /= len(m)
            center_of_cl.append(temp_coord)
        l_centroid.append(center_of_cl)
    if stop_criterion(l_centroid, centers) : break
    centers = l_centroid.copy()
    print("------------------------------------------------------------------------------------------------------------")


