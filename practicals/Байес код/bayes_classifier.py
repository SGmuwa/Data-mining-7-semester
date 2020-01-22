import numpy as np

# Чтение данных из файла
number_of_categorical_attribute = []
data=[]
with open(input("A filename: "), encoding = "utf-8") as file:
    number_of_categorical_attribute = file.readline().split(":")[1].split(",")
    target_var = int(file.readline().split(":")[1])
    number_of_classes = int(file.readline().split(":")[1])
    file.readline()
    for line in file:
        l = line.replace('\n', '').split("\t")
        for i in range(len(l)):
            try:
                l[i] = int(l[i])
            except ValueError:
                try:
                    l[i] = float(l[i])
                except:
                    l[i] = l[i]
        data.append(l)
print("Данные:\n", data)


number_of_column = len(data[0])
number_of_data = len(data)


# Функция map принимает два аргумента: функцию и аргумент составного типа данных, например, список. 
# map применяет к каждому элементу списка переданную функцию. 
number_of_categorical_attribute = list(map(int, number_of_categorical_attribute))

    
print("Категориальные признаки: {0}\nЦелевая переменная: {1}\nКоличество классов: {2}"
.format(number_of_categorical_attribute, target_var, number_of_classes))


# Чтение гипотезы
hypothesis_data = {}
with open(input("H filename: "), encoding = "utf-8") as f:
    line = f.readline().replace('\n', '').split("\t")
    attributes = list(range(number_of_column))
    del attributes[target_var]
    for num, attribute in zip(attributes, line):
            try:
                hypothesis_data[num] = int(attribute)
            except ValueError:
                try:
                    hypothesis_data[num] = float(attribute)
                except ValueError:  
                    hypothesis_data[num] = attribute
                    
print("Гипотеза: ", hypothesis_data)


# Получение уникальных значений столбцов
uniq_elements = []
for i in range(number_of_column):
    uniq_elements.append(set(d[i] for d in data))
print(uniq_elements)


count_el_of_class=[]
target_column = tuple(d[target_var] for d in data)
# Число объектов в разных классах
for c in uniq_elements[target_var]:
    count_el_of_class.append(target_column.count(c))
print("count_el_of_class", count_el_of_class)
# Вычисляем априорную вероятность появления класса
probability_classes = {}
for c in uniq_elements[target_var]:
    probability_classes[c] = len(list(filter(lambda x: x == c, target_column)))  / number_of_data
print("Априорная вероятность появления класса", probability_classes)

# Расчёт условных вероятностей
def get_count_of_set_in_train_data(data, number_of_att, att, class_):
    count = 0
    for id, row_data in enumerate(data):
        if(data[id][number_of_att] == att and data[id][target_var] == class_):
            count+=1
    return count

conditional_probabilities = {}
for ind_cl, cl in enumerate(uniq_elements[target_var]): # Для каждого класса
    cond_prob_for_class = []
    for att_ind in number_of_categorical_attribute: # Для категориальных атрибутов
        cond_prob_for_class.append((get_count_of_set_in_train_data(data, att_ind, hypothesis_data[att_ind], cl)) / count_el_of_class[ind_cl])
    conditional_probabilities[cl] = cond_prob_for_class
print("conditional_probabilities", conditional_probabilities)

#находим непрерыные атрибуты
continuous_attributes = {}
if len(number_of_categorical_attribute) + 1 < number_of_column:
    continuous_attributes = set([x for x in range(number_of_column)])
    continuous_attributes.difference_update(set(number_of_categorical_attribute))
    continuous_attributes.difference_update({target_var})
print(continuous_attributes)

import math
#Функция Гаусса
def getvalue_func_Gauss(x,m,d):
    return (1/((2*math.pi*d)**0.5)) * math.exp((-1)*( (x-m)**2  / 2*d))

# среднее значение и дисперсия Атрибута Ai для наблюдений относящихся к классу Ск
def get_dispersion_and_math_expected(column, cl):
    list_result = []
    for i in range(number_of_data):
        if data[i][target_var] == cl:
            list_result.append(data[i][column])
    return [np.mean(list_result), np.var(list_result)]  

cond_prob_for_continuous_attributes = {}
if(continuous_attributes!={}):
    for ind_cl,cl in enumerate(uniq_elements[target_var]):#Для каждого класса
        cb_for_class = []
        for c in continuous_attributes: # По столбцам (по непрерывным атрибутам)
            l_m_d = get_dispersion_and_math_expected(c, cl)
            val = getvalue_func_Gauss(hypothesis_data[c],l_m_d[0],l_m_d[1])
            cb_for_class.append(val)                               
        cond_prob_for_continuous_attributes[cl] = cb_for_class
print(cond_prob_for_continuous_attributes)


# Произведение условная вероятность и вероятность класса
result = {}
for k, v in conditional_probabilities.items():
    result[k] = probability_classes[k] * np.prod(v)
print(result)

