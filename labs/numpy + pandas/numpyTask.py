
import numpy as np
import sys
# Сгенерируйте матрицу, состоящую из 1000 строк и 50 столбцов, элементы которой являются случайными из нормального распределения 
# N(1,100). - 1 - среднее нормальное распределение, 100 - стандартное отклонение от нормального распределения
def Task1():
    print('Задание 1')
    np.set_printoptions(threshold=sys.maxsize)
    a = np.random.normal(loc = 1, scale = 100, size = (1000, 50) ) # однородный многомерный массив (бъект ndarray)
                                                                #loc - мат ожидание, scale σ — среднеквадратическое отклонение
                                                                #mu, sigma = 0, 0.1; s = np.random.normal(mu, sigma, 1000)
    return a

# 2. Произведите нормировку матрицы из предыдущего задания: вычтите из каждого столбца его среднее значение, а 
# затем поделите на его стандартное отклонение.
def Task2():
    a = Task1()
    print('Задание 2')
    for i in range(50): #Цикл по столбцам
        average_value = np.mean(a[:,i]) #среднее значение столбца (np.mean(a) #среднее арифметическое)
        standard_deviation = np.std(a[:,i]) # std = sqrt(mean(abs(x - x.mean())**2))   Стандартное отклонение представляет собой квадратный корень из среднего значения квадратов отклонений от среднего значения
        a[:,i] = (a[:,i] -  average_value) /  standard_deviation
    return a

#3. Выведите для заданной матрицы номера строк, сумма элементов в которых превосходит 10.
def Task3():
    print('Задание 3')
    a = Task2()
    output = []
    print("\n\nНомера строк, сумма элементов в которых превосходит 10:")
    for i in range(100):
        sum_str = np.sum(a[i,:])
        if sum_str>10:
            output.append(i)
    return output

#4. Сгенерируйте две единичные матрицы (т.е. с единицами на диагонали) размера 3x3. Соедините две матрицы в одну размера 6x3.
def Task4():
    print('Задание 4')
    print("\n\nДве единичные матрицы ")
    one1 = np.eye(3)
    one2 = np.eye(3)
    print("\n")
    print(one1)
    print("\n")
    print(one2)
    print("\n")
    #Несколько массивов могут быть объединены вместе вдоль разных осей с помощью функций hstack и vstack.
    one_rez = np.vstack((one1, one2))
    return one_rez

tasks = [Task1, Task2, Task3, Task4]
shift = 0
while not int(shift) in range(1, 5):
    shift = input("Выберите задание (1 ... 4) : ")
print(tasks[int(shift) - 1]())