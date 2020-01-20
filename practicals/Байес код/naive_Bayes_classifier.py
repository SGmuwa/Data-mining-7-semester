import numpy as np

# Чтение данных из файла
number_of_categorical_attribute = []
train_data=[]
with open("data_A.txt", encoding = "utf-8") as file:
    number_of_categorical_attribute = file.readline().split(":")[1].split(",")
    target_var = int(file.readline().split(":")[1])
    number_of_classes = int(file.readline().split(":")[1])
    file.readline()
    for line in file:
        l = line.split("\t")
        for i in range(len(l)):
            l[i] = l[i].strip("\t").lower().strip("\n")
        train_data.append(l)
data = np.array(train_data)
print("Данные:\n", data)


number_of_column = data.shape[1]
number_of_data = data.shape[0]


# Функция map принимает два аргумента: функцию и аргумент составного типа данных, например, список. 
# map применяет к каждому элементу списка переданную функцию. 
number_of_categorical_attribute = list(map(int, number_of_categorical_attribute))

    
print("Категориальные признаки: {0}\nЦелевая переменная: {1}\nКоличество классов: {2}"
.format(number_of_categorical_attribute, target_var, number_of_classes))


# Чтение гипотезы
hypothesis_data = {}
with open("data_H.txt", encoding = "utf-8") as f:
    line = f.readline().split("\t")
    for num, attribute in zip(number_of_categorical_attribute, line):
        hypothesis_data[num] = attribute
                    
print("Гипотеза: ", hypothesis_data)


# Получение уникальных значений столбцов
uniq_elements = []
for i in range(number_of_column):
    uniq_elements.append([i, np.unique(data[:,i], axis = 0)])
print(uniq_elements)


count_el_of_class=[]
# Число объектов в разных классах
for c in uniq_elements[target_var][1]:
    count_el_of_class.append(list(data[:,target_var]).count(c))
print("count_el_of_class", count_el_of_class)
# Вычисляем априорную вероятность появления класса
probability_classes = []
for c in uniq_elements[target_var][1]:
    probability_classes.append(len(list(filter(lambda x: x == c, data[:,target_var])))  / number_of_data )
print("Априорная вероятность появления класса", probability_classes)

# Расчёт условных вероятностей
def get_count_of_set_in_train_data(number_of_att, att, class_):
    count = 0
    for id, row_data in enumerate(data):
        if(data[id, number_of_att] == att and data[id, target_var] == class_):
            count+=1
    return count

conditional_probabilities = []
for ind_cl,cl in enumerate(uniq_elements[target_var][1]): # Для каждого класса
    cond_prob_for_class = []
    for att_ind in number_of_categorical_attribute: # Для категориальных атрибутов
        cond_prob_for_class.append((get_count_of_set_in_train_data(att_ind, hypothesis_data[att_ind], cl)) / count_el_of_class[ind_cl])
    conditional_probabilities.append([cl, cond_prob_for_class])
print(conditional_probabilities)



# среднее значение и дисперсия Атрибута Ai для наблюдений относящихся к классу Ск
def get_dispersion_and_math_expected(column, cl):
    list_result = []
    for i, el in enumerate(number_of_data):
        if data[i,target_var] == cl:
            list_result.append(data[i,column])
    return [np.mean(list_result), np.var(list_result)]  



# Произведение условная вероятность и вероятность класса
result = []
for ind,el in enumerate(conditional_probabilities):
    result.append([el[0], probability_classes[ind] * np.prod(el[1])])
print(result)

