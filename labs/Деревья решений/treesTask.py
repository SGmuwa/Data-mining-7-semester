# Импортируем дерево решений для классификации
import numpy as np
import sklearn
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

print(
'''
1. Загрузите выборку из файла titanic.csv с помощью пакета Pandas.
2. Оставьте в выборке четыре признака: класс пассажира (Pclass), цену билета (Fare), возраст пассажира (Age) и его пол (Sex).
3. Обратите внимание, что признак Sex имеет строковые значения.
4. Выделите целевую переменную — она записана в столбце Survived.
5. В данных есть пропущенные значения — например, для некоторых пассажиров неизвестен их возраст. Такие записи при чтении их в pandas принимают значение nan. Найдите все объекты, у которых есть пропущенные признаки, и удалите их из выборки.
6. Обучите решающее дерево с параметром random_state=241 и остальными параметрами по умолчанию.
7. Вычислите важности признаков и найдите два признака с наибольшей важностью. Их названия будут ответами для данной задачи
(в качестве ответа укажите названия признаков через запятую без
пробелов).
''')

# 1. Загрузите выборку из файла titanic.csv с помощью пакета Pandas.
def Task1():
    return pd.read_csv('titanic.csv', sep=',')

# 2. Оставьте в выборке четыре признака: класс пассажира (Pclass), цену билета (Fare), возраст пассажира (Age) и его пол (Sex).
def Task2():
    data = Task1()
    data_short = pd.DataFrame(data, columns  = ['Pclass', 'Fare', 'Age', 'Sex'])
    return (data, data_short)

# 5. В данных есть пропущенные значения — например, для некоторых
# пассажиров неизвестен их возраст. Такие записи при чтении их в
# pandas принимают значение nan. Найдите все объекты, у которых
# есть пропущенные признаки, и удалите их из выборки.
def Task5():
    (data, data_short) = Task2()
    data_short = data_short.dropna()
    return (data, data_short)

# 3. Обратите внимание, что признак Sex имеет строковые значения.
def Task3():
    (data, data_short) = Task5()
    data_short['Sex'].replace(['male', 'female'], [1, 0], inplace=True)
    return (data, data_short)

# 4. Выделите целевую переменную — она записана в столбце Survived.
def Task4():
    (data, data_short) = Task3()
    d_y = pd.DataFrame(data,columns = ['Survived','Age'])
    d_y = d_y.dropna()
    del d_y['Age']
    return (data_short, d_y)

#data_short = np.array(data_short)
#d_y = np.array(d_y)

# 6. Обучите решающее дерево с параметром random_state=241 и остальными параметрами по умолчанию.
def Task6():
    clf = DecisionTreeClassifier(random_state = 241)
    (data_short, d_y) = Task4()
    clf.fit(data_short, d_y)
    return clf

# 7. Вычислите важности признаков и найдите два признака с наибольшей важностью.
# Их названия будут ответами для данной задачи
# (в качестве ответа укажите названия признаков через запятую без пробелов).
def Task7():
    clf = Task6()
    importances = pd.Series(clf.feature_importances_, index=['Pclass', 'Fare', 'Age', 'Sex'])

    X = [[1,2], [3, 4], [5, 6]] # обучающие выборки (3 элемента в обучающей выборке (3 строки) с двумя признаками)
    Y = [0, 1,0] # содержит метки классов для обучающей выбороки
    clf = sklearn.tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)
    clf.predict([[2., 2.]])
    return (importances, sklearn.tree.export_text(clf.fit(X,Y)))

tasks = [Task1, Task2, Task3, Task4, Task5, Task6, Task7]
shift = 0
while not int(shift) in range(1, len(tasks) + 1):
    shift = input("Выберите задание (1 ... 7) : ")
for a in tasks[int(shift) - 1]():
    print(a)
