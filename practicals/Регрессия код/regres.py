# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import matplotlib.pyplot as plt
import numpy as np 
import random as rd 

func = lambda x : -36 * x + 823


# %%
x = np.linspace(0, 100, 100)
y = func(x)
new_x = [rd.randint(0,100) for i in range(15)]
new_y = [func(i) + rd.randint(-500, 500) for i in new_x]

plt.plot(x, y)
plt.plot(new_x, new_y, 'o')


# %%
a = new_x
b = new_y
b1 =(sum([i * g for i, g in zip(a, b)]) - (sum(a) * sum(b)) / (len(a))) / (sum([i ** 2 for i in a]) - (sum(a) ** 2 ) / (len(a)))
b1


# %%
b0 = sum(new_y) / len(new_x) - b1 * sum(new_x) / len(new_x)
b0


# %%
new_func = lambda x : b1 * x + b0


# %%
plt.plot(x, y)
plt.plot(x, new_func(x))
plt.plot(new_x, new_y, 'o')


# %%
# среднеквадратичная
m = 1
y_ = [new_func(i) for i in new_x]
Ecko = (sum([(a - b) ** 2 for a, b in zip(new_y, y_)])) / (len(new_x) - m - 1)
Ecko


# %%
# стандартная
Ect = Ecko ** 1/2
Ect


# %%
# изменчивость
y_sr = sum(new_y) / len(new_y)
Q = sum((a - y_sr) ** 2 for a in new_y)
Q


# %%
Qr = sum((new_func(b) - y_sr) ** 2 for b in new_x)
Qr


# %%
Qe = sum((a - new_func(b)) ** 2 for a ,b in zip(new_y, new_x))
Qe


# %%
# Коэф детерминации
r2 = Qr / Q
r2


# %%
# Коэф корреляции
r = 0
if b1 > 0:
    r = r2 ** 1/2
else:
    r = -(r2 ** 1/2)
r


# %%



# %%


