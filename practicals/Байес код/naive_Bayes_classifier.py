import numpy as np

# Чтение данных из файла
number_of_categorical_attribute = []
train_data=[]
with open("lect_data.txt", encoding = 'utf-8') as file:
    number_of_categorical_attribute = file.readline().split(":")[1].split(",")
    target_var = int(file.readline().split(":")[1])
    number_of_classes = int(file.readline().split(":")[1])
    for line in file:
        l = line.split(' ')
        for i in range(len(l)):
            try:
                l[i] = int(l[i].strip(" ").lower().strip("\n"))
            except ValueError:
                try:
                    l[i] = float(l[i].strip(" ").lower().strip("\n"))
                except ValueError:  
                    l[i] = l[i].strip(" ").lower().strip("\n")
        train_data.append(l)
data = np.array(train_data)
print("Данные:\n", data)


number_of_column = data.shape[1]
number_of_data = data.shape[0]


#Функция map принимает два аргумента: функцию и аргумент составного типа данных, например, список. 
#map применяет к каждому элементу списка переданную функцию. 
number_of_categorical_attribute = list(map(int, number_of_categorical_attribute))

    
print("Категориальные признаки: {0}\nЦелевая переменная: {1}\nКоличество классов: {2}"
.format(number_of_categorical_attribute, target_var, number_of_classes))


#Чтение тестовых данных
test_data = []
with open("lk_data_test.txt", encoding = 'utf-8') as f:
    for line in f:
        test_data = line.split(' ')
        for i in range(len(test_data)):
            try:
                test_data[i] = int(test_data[i].strip(" ").lower().strip("\n"))
            except ValueError:
                try:
                    test_data[i] = float(test_data[i].strip(" ").lower().strip("\n"))
                except ValueError:  
                    test_data[i] = test_data[i].strip(" ").lower().strip("\n")
print("Тестовые данные: ", test_data)


# Получение уникальных значений столбцов
uniq_elements = []
for i in range(number_of_column):
    uniq_elements.append([i,np.unique(data[:,i],axis = 0)])
print(uniq_elements)


count_el_of_class=[]
# Число объектов в разных классах
for c in uniq_elements[target_var][1]:
    count_el_of_class.append(list(data[:,target_var]).count(c))
print('count_el_of_class', count_el_of_class)
# Вычисляем априорную вероятность появления класса
probability_classes = []
for c in uniq_elements[target_var][1]:
    probability_classes.append(len(list(filter(lambda x: x == c, data[:,target_var])))  / number_of_data )
print("Априорная вероятность появления класса", probability_classes)


# Расчёт условных вероятностей
def get_count_of_set_in_train_data(number_of_att, att, class_):
    count = 0
    for id, row_data in enumerate(data):
        if(data[id,number_of_att] == att and data[id,target_var] == class_):
            count+=1
    return count

conditional_probabilities = []
for ind_cl,cl in enumerate(uniq_elements[target_var][1]):#Для каждого класса
    cond_prob_for_class = []
    for att_ind in number_of_categorical_attribute:  #Для категориальных атрибутов
        cond_prob_for_class.append((get_count_of_set_in_train_data(att_ind,test_data[att_ind],cl)) / count_el_of_class[ind_cl]) # 0 "жарко" и "да"
    conditional_probabilities.append([cl,cond_prob_for_class])
print(conditional_probabilities)


# находим непрерывные атрибуты
continuous_attributes = {}
if len(number_of_categorical_attribute) + 1 < number_of_column:
    continuous_attributes = set([x for x in range(number_of_column)])
    continuous_attributes.difference_update(set(number_of_categorical_attribute))
    continuous_attributes.difference_update(set(target_var))
print('continuous_attributes', continuous_attributes)

import math
# Функция Гаусса
def getvalue_func_Gauss(x, m, d):
    return (1 / ((2 * math.pi * d) ** 0.5)) * math.exp(-1 * ((x - m) ** 2 / 2 * d))


# среднее значение и дисперсия Атрибута Ai для наблюдений относящихся к классу Ск
def get_dispersion_and_math_expected(column, cl):
    list_result = []
    for i, el in enumerate(number_of_data):
        if data[i,target_var] == cl:
            list_result.append(data[i,column])
    return [np.mean(list_result), np.var(list_result)]  


cond_prob_for_continuous_attributes = []
if(continuous_attributes!={}):
    for ind_cl,cl in enumerate(uniq_elements[target_var][1]): # Для каждого класса
        cb_for_class = []
        for c in continuous_attributes: # По столбцам (по непрерывным атрибутам)
            l_m_d = get_dispersion_and_math_expected(c, cl)
            val = getvalue_func_Gauss(test_data[c], l_m_d[0], l_m_d[1])
            cb_for_class.append(val)                               
        cond_prob_for_continuous_attributes.append([cl, cb_for_class])
print('cond_prob_for_continuous_attributes', cond_prob_for_continuous_attributes)


for ind,el in enumerate(conditional_probabilities):
    if cond_prob_for_continuous_attributes !=[]:
        conditional_probabilities[ind][1] = conditional_probabilities[ind][1] + cond_prob_for_continuous_attributes[ind][1]
    


#Произведение условная вероятность и вероятность класса
result = []
for ind,el in enumerate(conditional_probabilities):
    result.append([el[0], probability_classes[ind] * np.prod(el[1])])
print(result)

