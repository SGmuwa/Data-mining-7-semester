import numpy as np
import matplotlib.pyplot as plt
number_of_clusters = 4
m = 1
# Чтение данных из файла
clustered_elements=[]
# данные зависимости потребления Y (усл. ед.) от дохода X (усл.ед.) для некоторых домашних хозяйств. 
f = open(input("filename: "), encoding = 'utf-8-sig')
for line in f:
    columns = line.strip("\n").split('\t')
    for i in range(len(columns)):
        columns[i] = float(columns[i])
    clustered_elements.append(columns)
data = np.array(clustered_elements)
print(data)


# Находим уравнение линии регрессии y` = b0 + b1*x
# Сначала находим b1

b1 = 10 * np.sum(data[:, 0] * data[:, 1]) - (np.sum(data[:, 0]) * np.sum(data[:, 1]))
b1 /= ((np.sum(data[:, 0] ** 2) * 10 - np.sum(data[:, 0]) ** 2))
print("b1 = ", b1)
# Находим b0
b0 = np.sum(data[:, 1]) / data.shape[0] - (b1 / data.shape[0]) * np.sum(data[:, 0])
print("b0 = ", b0)

x = np.linspace(data[:, 0].min(), data[:, 0].max())
y = b0 + (b1 * x)
plt.title("График зависимости входной переменной X от Y") # заголовок
plt.plot(data[:, 0], data[:, 1], "ro", x, y) # построение графика
plt.xlabel("x") # ось абсцисс
plt.ylabel("y") # ось ординат
plt.grid()      # включение отображение сетки
plt.show()


# Вычислим значение y` предсказанное сетью и запишим данные и предсказанные значения в matrix
def pred(x):
    return b0 + b1 * x
array_y_pred = []
for idx, item in enumerate(data[:, 0]):
    t = pred(item)
    array_y_pred.append([t,])
matrix = np.hstack((data, np.array(array_y_pred)))
print(matrix)



# Оценка соответствия простой линейной регрессии реальным данным
# Стандартная ошибка оценки
st_e = ((matrix[:, 1] - matrix[:, 2]) ** 2).sum()
st_e /= (data.shape[0] - m - 1)
st_e = st_e ** 0.5
print("Стандартная ошибка оценки = ", st_e, "\nМера разброса точек наблюдений относительной линии регрессии (показывает среднюю величину отклонения точек исходных данных от линий регрессии вдоль оси Y)")

mean_y = np.mean(data, axis=0)[1] #mean_y = np.mean(data, axis=0)   -  среднии значения столбцов
e_st_mean = ((1 / (data.shape[0] - 1)) * ((matrix[:, 1] - mean_y) ** 2).sum()) ** 0.5
print("Ошибка относительно среднего значения = ", e_st_mean, "\nПрименение регрессии вместо оценки на основе простого среднего значения позволяет уменьшить ошибку более чем в 4 раза.")
print("Отношение", e_st_mean / st_e)


# три квадратичные суммы
# общая полная
Q = ((matrix[:, 1] - mean_y) ** 2).sum()
Q_r = ((matrix[:, 2] - mean_y) ** 2).sum()
Q_e = ((matrix[:, 1] - matrix[:, 2]) ** 2).sum()
print("Q = ", Q)
if Q_r + Q_e != Q: raise NameError("Q != Q_r + Q_e", Q, " != ", Q_r + Q_e)


# Коэффициент детерминации
r_squared = Q_r / Q
print("Коэффициент детерминации", r_squared, "\nПоказывает степень согласия регрессии как приближение линейного отношения между входной и выходной переменными с реальными данными")


#Коэффициент корреляции
x_mean = np.mean(data, axis = 0)[0]
std_x = np.std(data[:, 0]) # std = sqrt(mean(abs(x - x.mean()) ** 2)) 
std_y = np.std(data[:, 1])
r = ((data[:, 0] - x_mean) * (data[:, 1] - mean_y)).sum()
r /= ((data.shape[0]) * std_x * std_y)
print("Коэффициент корреляции = ", r, "\nИспользуется для количественного описания линейной зависимости между двумя числовыми переменными")
print("Коэффициент корреляции = корень из Коэффициент детерминации", r_squared ** 0.5 if(b1>0) else -(r_squared ** 0.5))
