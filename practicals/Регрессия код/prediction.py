# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import matplotlib.pyplot as plt
number_of_clusters = 4
m = 1
#Чтение данных из файла
clustered_elements=[]
#данные зависимости потребления Y (усл. ед.) от дохода X (усл.ед.) для некоторых домашних хозяйств. 
f = open("dependence_of_sales_on_price.txt", encoding = 'utf-8')
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
plt.title("График зависимости входной переменной X от Y") # заголовок
plt.plot(data[:,0], data[:,1],"ro") # построение графика
plt.xlabel("x") # ось абсцисс
plt.ylabel("y") # ось ординат
plt.grid()      # включение отображение сетки


# %%
#Находим уравнение линии регрессии y` = b0 + b1*x
#Сначала находим b1

b1 = 10 * np.sum(data[:,0] * data[:,1]) - (np.sum(data[:,0]) * np.sum(data[:,1]))
b1 /= ((np.sum(data[:,0] ** 2)*10 - np.sum(data[:,0]) ** 2))
print("b1 = ",b1)
#Находим b0=
b0 = np.sum(data[:,1]) / data.shape[0]  -  (b1/data.shape[0])*np.sum(data[:,0])
print("b0 = ",b0)

x = np.linspace(data[:,0].min(), data[:,0].max())
y =b0 + (b1*x)
plt.title("График зависимости входной переменной X от Y") # заголовок
plt.plot(data[:,0], data[:,1],"ro",x,y) # построение графика
plt.xlabel("x") # ось абсцисс
plt.ylabel("y") # ось ординат
plt.grid()      # включение отображение сетки


# %%
#Вычислим значение y` предсказаннное сетью и запишим данные и предсказанные значения в matrix
def pred(x):
    return b0+b1*x
array_y_pred = []
for idx, item in enumerate(data[:,0]):
    t = pred(item)
    array_y_pred.append([t,])
matrix = np.hstack((data, np.array(array_y_pred)))
print(matrix)



#Оценка соответсвия простой линейной регрессии реальным данным
#Стандарная ошибка оценивания
st_e = ((matrix[:,1] - matrix[:,2])**2).sum()
st_e/=(data.shape[0] - m - 1)
st_e = st_e**0.5
print("Стандартная ошибка = ",st_e)

mean_y = np.mean(data, axis=0) [1] #mean_y = np.mean(data, axis=0)   -  среднии значения столбцов
#print(mean_y)
e_st_mean = ((1/(data.shape[0] - 1)) * ((matrix[:,1] - mean_y)**2).sum())**0.5
print("Ошибка относительно среднего значения = ",e_st_mean)
print("Отношение",e_st_mean/st_e)


#три квадратичные суммы
#общая полная
Q = ((matrix[:,1] - mean_y)**2).sum()
Q_r = ((matrix[:,2] - mean_y)**2).sum()
Q_e = ((matrix[:,1] - matrix[:,2])**2).sum()
print(Q_r,Q_e)
print("Q = Q_r + Q_e:  ",Q," = ",Q_r+Q_e)


#Коэффициент детерминации
r_squared = Q_r/Q
print("Коэффициент детерминации",r_squared)


#Коэффициент корреляции
x_mean = np.mean(data, axis=0) [0]
std_x =  np.std(data[:,0])#std = sqrt(mean(abs(x - x.mean())**2)) 
std_y = np.std(data[:,1])#std = sqrt(mean(abs(x - x.mean())**2)) 
r = ((data[:,0]-x_mean) * (data[:,1]-mean_y)).sum()
r/= ((data.shape[0])*std_x*std_y)
print("Коэффициент корреляции = ",r)
print("Коэффициент корреляции = корень из Коэффициент детерминации", r_squared**0.5 if(b1>0) else (r_squared**0.5)*(-1))


# %%
sequence = [1, 2, 7, 19]
# Сравните:
idx = 0
for item in sequence:
    print(idx)
    idx += 1

# и
for idx, item in enumerate(sequence):
    print(idx,item)
      
arr=np.array([[1,2,3],[4,5,6]])

arr.tolist()

