import matplotlib.pyplot as plt
import numpy as np 
import random as rd 

data = np.genfromtxt(input("filename: "), delimiter='\t', encoding='utf-8-sig')

x = data[:, 0]
y = data[:, 1]

x_mean = np.mean(x)
y_mean = np.mean(y)
b1up = sum([(x_ - x_mean)*(y_ - y_mean) for x_, y_ in zip(x, y)])
b1down = sum([(x_ - x_mean)**2 for x_ in x])
b1 = b1up / b1down
print('b1up', b1up, 'b1down', b1down)
print('b1', b1)


b0 = y_mean - b1 * x_mean
print('b0', b0)


new_func = lambda x : b1 * x + b0


plt.plot(x, y, 'o')
plt.plot(x, new_func(x))
plt.show()


# Среднеквадратичная ошибка
m = 1
y_ = [new_func(i) for i in x]
Ecko = (sum([(a - b) ** 2 for a, b in zip(y, y_)])) / (len(x) - m - 1)
print('Среднеквадратичная ошибка', Ecko)


# Стандартная ошибка
Ect = Ecko ** 1/2
print('Стандартная ошибка Ect', Ect)


# Изменчивость
y_sr = sum(y) / len(y)
Q = sum((a - y_sr) ** 2 for a in y)
print('Изменчивость Q', Q)


Qr = sum((new_func(b) - y_sr) ** 2 for b in x)
print('Qr', Qr)


Qe = sum((a - new_func(b)) ** 2 for a ,b in zip(y, x))
print('Qe', Qe)


# Коэффициент детерминации
r2 = Qr / Q
print('Коэффициент детерминации r2', r2)


# Коэффициент корреляции
r = 0
if b1 > 0:
    r = r2 ** 1/2
else:
    r = -(r2 ** 1/2)
print('Коэффициент корреляции r', r)
