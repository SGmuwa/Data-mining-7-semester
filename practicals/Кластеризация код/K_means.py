# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import pandas as pd
number_of_clusters = 4
#Чтение данных из файла
clustered_elements=[]
f = open("data_for_k_means", encoding = 'utf-8')
for line in f:
    l = line.split(' ')
    for i in range(len(l)):
        try:
            l[i] = int(l[i].strip(" ").lower().strip("\n"))
        except ValueError:
            l[i] = float(l[i].strip(" ").lower().strip("\n"))
    clustered_elements.append(l)
data = np.array(clustered_elements)
print(data)


# %%
#Нормализация данных (Представление в виде от 0 до 1):  x_normed = (x - x.min(0)) / x.ptp(0)
# print(np.ptp(data, axis=0))
# for i in range(data.shape[1]):
#     data[:,i] =( data[:,i] - data[:,i].min() ) / np.ptp(data, axis=0)[i] #все строки i-ого столбца
# print(data)

#для numpy
# for i in range(data.shape[1]): #Цикл по столбцам
#     average_value = np.mean(data[:,i]) #среднее значение столбца (np.mean(a) #среднее арифметическое)
#     standard_deviation = np.std(data[:,i]) # std = sqrt(mean(abs(x - x.mean())**2))   Стандартное отклонение представляет собой квадратный корень из среднего значения квадратов отклонений от среднего значения
#     data[:,i] = (data[:,i] -  average_value) /  standard_deviation
# print(data)


# %%
#ТЕСТ на нормализацию 
mean = data.mean(axis = 0)
std = data.std(axis=0)
data-=mean
data /= std
print(data)

data.mean(axis = 0)
data.std(axis = 0)


# %%
def get_euclidean_distance (l1,l2):
    euclid = 0
    count = len(l1)
    for i in range(count):
        euclid += (l1[i]-l2[i])**2
    return euclid ** 0.5

list_for_serch_start_centers = []

#Центроид для всех данных:
centroid = (data.sum(axis = 0))/data.shape[0]
print(centroid)

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


# %%
# Алгоритм К-средних
import random
ind_centers = random.sample(list(range(data.shape[0])), number_of_clusters)
cluster_numbers = list(range(number_of_clusters))#Номера кластеров
print(ind_centers)
#ind_centers = [18, 1, 8, 3]
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


# %%
#ТЕСТ
print((-1.32911564+(-1.32911564))/2)
el = [1,[1,7]]
m = el[1]
num_center_of_cl = data.shape[1] #число координат центра
center_of_cl = []
    
for i in range(num_center_of_cl):#Для каждок координаты центра
    temp_coord = 0 
    for j in m:
        print("data[j,i]",data[j,i])
        temp_coord+=data[j,i]
    temp_coord /= len(m)
    center_of_cl.append(temp_coord)
print(center_of_cl)
[0.20865709 -1.24771194 -0.93799953 -1.32911564]
[-0.17977678 -1.61740437 -1.14750196 -1.32911564]


# %%
import numpy as np
x = np.array([[0, 1], 
              [2, 3]]) 

print(np.ptp(x, axis=0)) #0 - ось столбцов np.ptp(x, axis=1) #0 - ось столбцов

x[:,1] =( x[:,1] - x[:,1].min() ) / np.ptp(x, axis=0)[1] #все строки i-ого столбца
print(x)


# %%
b = np.array([[1, 2, 3], 
              [4, 5, 6]])
for i in range(b.shape[1]): #Цикл по столбцам
    average_value = np.mean(b[:,i]) #среднее значение столбца (np.mean(a) #среднее арифметическое)
    standard_deviation = np.std(b[:,i]) # std = sqrt(mean(abs(x - x.mean())**2))   Стандартное отклонение представляет собой квадратный корень из среднего значения квадратов отклонений от среднего значения
    b[:,i] = (b[:,i] -  average_value) /  standard_deviation
print(b)


for i in b:
    print(type(i))


# %%
center_of_cl = [None]*5
len(center_of_cl)


# %%
b = [[1, 2, 3], [4, 5, 6]]
a = b.copy()
print(a)
#Списки равны, если элементы с одинаковым индексом равны. Учитывается порядок.
print("a==b",a==b)
aaaaaaaaa = []
print("c==[]",len(aaaaaaaaa)==0)
print("a==c",a==c)


# %%
g1 = [[0.5842459288630132, 0.41590398067525874, 0.4761418927616714, -0.3271032249022722], [0.014440155331363919, -1.4325581556592244, -1.0427507451480607, -1.3291156353623974], [-0.33136532628503307, -0.7034425352161782, -0.7168580718800721, -0.23601118758771536], [-0.11041358945510202, 1.3401350488425003, 1.1360745561293482, 1.3489902616855738]]
g2 = [ [0.014440155331363919, -1.4325581556592244, -1.0427507451480607, -1.3291156353623974], [-0.33136532628503307, -0.7034425352161782, -0.7168580718800721, -0.23601118758771536], [-0.11041358945510202, 1.3401350488425003, 1.1360745561293482, 1.3489902616855738]]
print(g1==g2)
student_tuples = [
        ('john', 'A', 15),
        ('jane', 'B', 12),
        ('dave', 'B', 10),
    ]
sor = sorted(student_tuples, key=lambda student: student[2])   # сортируем по возрасту
print(sor)


