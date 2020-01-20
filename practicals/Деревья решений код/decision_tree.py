import pandas as pd
import numpy as np

# 1. Загрузите выборку из файла titanic.csv с помощью пакета Pandas.
df = pd.read_csv('titanic.csv', sep=',')
# 2. Оставьте в выборке четыре признака: класс пассажира (Pclass), цену билета (Fare), возраст пассажира (Age) и его пол (Sex).
dataset = pd.DataFrame(df,columns  = ['Pclass','Fare','Age','Sex','Survived'])
# 5. В данных есть пропущенные значения — например, для некоторых
# пассажиров неизвестен их возраст. Такие записи при чтении их в
# pandas принимают значение nan. Найдите все объекты, у которых
# есть пропущенные признаки, и удалите их из выборки.
dataset = dataset.dropna()
# 3. Обратите внимание, что признак Sex имеет строковые значения.
dataset['Sex'].replace(['male', 'female'], [1, 0], inplace=True)


#как преобразовать в массив numpy для деревьев
dataset = np.array(dataset)
print(dataset)
dataset = dataset.tolist()
print(dataset)
# алгоритм CART (Classification and Regression Tree)
from random import seed
from random import randrange
from csv import reader

# Разделить набор данных на k 
def cross_validation_split(dataset, n_folds):
    dataset_split = list()
    dataset_copy = list(dataset)
    fold_size = int(len(dataset) / n_folds)
    for i in range(n_folds):
        fold = list()
        while len(fold) < fold_size:
            index = randrange(len(dataset_copy))
            fold.append(dataset_copy.pop(index))
        dataset_split.append(fold)
    return dataset_split

# Рассчитать процент точности
def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0

# Оценить алгоритм с использованием разделения перекрестной проверки
def evaluate_algorithm(dataset, algorithm, n_folds, *args):
    folds = cross_validation_split(dataset, n_folds)
    scores = list()
    for fold in folds:
        train_set = list(folds)
        train_set.remove(fold)
        train_set = sum(train_set, [])
        test_set = list()
        for row in fold:
            row_copy = list(row)
            test_set.append(row_copy)
            row_copy[-1] = None
        predicted = algorithm(train_set, test_set, *args)
        actual = [row[-1] for row in fold]
        accuracy = accuracy_metric(actual, predicted)
        scores.append(accuracy)
    return scores
# Разделить набор данных на основе атрибута и значения атрибута
def test_split(index, value, dataset):
    left, right = list(), list()
    for row in dataset:
        if row[index] <= value:
            left.append(row)
        else:
            right.append(row)
    return left, right

# Рассчитать индекс Джини для набора разделенных данных
# https://ru.wikipedia.org/wiki/Обучение_дерева_решений#Примесь_(критерий)_Джини 
# https://books.google.ru/books?id=5giqDwAAQBAJ&pg=PA94&lpg=PA94&dq=avoid+divide+by+zero+score+the+group+based+on+the+score+for+each+class&source=bl&ots=GxTEBQUJIc&sig=ACfU3U0c8H8kkQ5_x9UZryi9Vv_d-xncMA&hl=ru&sa=X&ved=2ahUKEwii89y2vZLnAhUFpIsKHSGkBm4Q6AEwAHoECAYQAQ#v=onepage&q=avoid%20divide%20by%20zero%20score%20the%20group%20based%20on%20the%20score%20for%20each%20class&f=false
def gini_index(groups, classes):
    # count all samples at split point
    n_instances = float(sum([len(group) for group in groups]))
    # sum weighted Gini index for each group
    gini = 0.0
    for group in groups:
        size = float(len(group))
        # avoid divide by zero
        if size == 0:
            continue
        score = 0.0
        # score the group based on the score for each class
        for class_val in classes:
            p = [row[-1] for row in group].count(class_val) / size
            score += p * p
        # weight the group score by its relative size
        gini += (1.0 - score) * (size / n_instances)
    return gini

# Выбор лучшей точки разделения для набора данных
def get_split(dataset):
    class_values = list(set(row[-1] for row in dataset))
    b_index, b_value, b_score, b_groups = 999, 999, 999, None
    for index in range(len(dataset[0])-1):
        for row in dataset:
            groups = test_split(index, row[index], dataset)
            gini = gini_index(groups, class_values)
            if gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index':b_index, 'value':b_value, 'groups':b_groups,'count_value_class':[len(g) for g in b_groups]}

# Создать значение терминального узла (листа)
def to_terminal(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)

# Создать дочерние разбиения для узла или сделать терминал (лист)
def split(node, max_depth, min_size, depth):
    left, right = node['groups']
    del(node['groups'])
    # check for a no split
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        return
    # check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        return
    # process left child
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        node['left'] = get_split(left)
        split(node['left'], max_depth, min_size, depth+1)
    # process right child
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        node['right'] = get_split(right)
        split(node['right'], max_depth, min_size, depth+1)

# Построить дерево решений
def build_tree(train, max_depth, min_size):
    root = get_split(train)
    split(root, max_depth, min_size, 1)
    return root

# Сделать прогноз с помощью дерева решений
def predict(node, row):
    if row[node['index']] <= node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']

# Алгоритм
def decision_tree(train, test, max_depth, min_size):
    tree = build_tree(train, max_depth, min_size)
    print("-----------------------------------------------------")
    print_tree(tree)
    predictions = list()
    for row in test:
        prediction = predict(tree, row)
        predictions.append(prediction)
    return(predictions)

# Print a decision tree
def print_tree(node, depth=0):
    if isinstance(node, dict):
        print('%s[X%d <= %.3f]' % ((depth*'   ', (node['index']+1), node['value'])),node["count_value_class"])
        print_tree(node['left'], depth+1)
        print_tree(node['right'], depth+1)
    else:
        print('%s[%s]' % ((depth*'   ', node)))
seed(241)

# Оценка построенного дерева
n_folds = 5
max_depth = 7
min_size = 10
scores = evaluate_algorithm(dataset, decision_tree, n_folds, max_depth, min_size)
print('Важность: %s' % scores)
print('Точность: %.3f%%' % (sum(scores)/float(len(scores))))