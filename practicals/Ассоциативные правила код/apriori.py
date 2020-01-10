#!/usr/bin/env python
# coding: utf-8

COUNT_OF_FREQUENT_SETS = 4
#Чтение транзакций из файла
transaction_list=[]
item_list=[]
f = open("transactions.txt", encoding = 'utf-8')
for line in f:
    l = line.split(',')
    for i in range(len(l)):
        l[i] = l[i].strip(" ").lower().strip("\n")
    transaction_list.append(l)
print("transaction_list:",transaction_list)


for el in transaction_list:
    for e in el:
        if (item_list.count(e)==0):
            item_list.append(e)
item_list.sort()
print("item_list",item_list)


#Нормированный вид множество транзакций
#item_list ['кабачки', 'капуста', 'кукуруза', 'перец', 'помидоры', 'спаржа', 'фасоль']
import numpy as np
normal_tranz = []
for tr in transaction_list:
    list_temp = []
    for i in item_list:
        list_temp.append(i) if (tr.count(i)>0) else  list_temp.append(0)
    normal_tranz.append(list_temp)
    
for i in range(len(normal_tranz)):
    print(normal_tranz[i])




#Количество набора в транзакциях
def get_count_of_set_in_transaction(set):
    count = 0
    for row_tr in normal_tranz:
        flag = True
        for el in set:
            if (row_tr.count(el)==0):
                flag = False
                break
        if flag: count+=1
    return count

list = ['фасоль', 'кабачки']
print("test",get_count_of_set_in_transaction(list))


#Однопредметные наборы
frequent_one_set = []
for it in item_list:
    print(get_count_of_set_in_transaction([it]))
    if get_count_of_set_in_transaction([it]) >= COUNT_OF_FREQUENT_SETS:
        frequent_one_set.append(it)
        
print(frequent_one_set)



#Поиск частых наборов

#Оставляет в списке только уникальные элементы
def unique(l):
    n = []
    for i in l:
        if i not in n:
            n.append(i)
    return n


#Получает на вход наборы, Возвращает только те наборы, количество которых в транзакциях больше COUNT_OF_FREQUENT_SETS
def get_abbreviated_set(sets):
    set_result = []
    for s in sets:
        if get_count_of_set_in_transaction(s)>=COUNT_OF_FREQUENT_SETS:
            set_result.append(s)
    return set_result

#Общие элементы двух наборов (в правильном количестве, например для ['кабачки', 'капуста'], [ 'кабачки', 'перец'] должен быть один общий элемент), иначе False
def get_n_common_elements(set1,set2):#n общих должны иметь
    common_elements = []
    n_common  = len(set1)-1
    for s1 in set1:
        for s2 in set2:
            if s2==s1: common_elements.append(s1); break
    if len(common_elements)==n_common: return common_elements
    else: return False

#Соединение наборов с помощью общих элементов
def merging_sets(set1,set2,common_elements):
    result_set = []
    for el_com in common_elements:
        result_set.append(el_com)
    for s1 in set1:
        if result_set.count(s1)==0:
            result_set.append(s1)
    for s2 in set2:
        if result_set.count(s2)==0:
            result_set.append(s2)
    return result_set

def get_set_k(k,list):
    set_k_candidates = []
    number_of_common = k - 1
    set_k=[]
    
    if number_of_common==0:
        for i in range(len(list)-1):
            for j in range(i+1,len(list)):
                set_k_candidates.append([list[i],list[j]])
        set_k =  get_abbreviated_set(set_k_candidates)
        return set_k
    
    
    if number_of_common>=1: #Например, для связывания двух двухэлементных наборов, они должны иметь один общий элемент
        for i in range(len(list)-1):
            for j in range(i+1,len(list)):
                common_elements = get_n_common_elements(list[i],list[j])
                if (not common_elements == False):
                    set_k_candidates.append(merging_sets(list[i],list[j],common_elements))
        for el in set_k_candidates:
             el = el.sort()
        set_k_candidates = unique(set_k_candidates)
        
        
        #Проверим найденные наборы 
        #Создаем списки размером k (для проверки набора с помощью свойства анти-монотонности)
        for c in set_k_candidates:
            temp_for_check = []
            for i in range(len(c)-1):
                for j in range(i+1,len(c)):
                    temp_for_check.append([c[i],c[j]])
            
            if(temp_for_check == get_abbreviated_set(temp_for_check)): set_k.append(c)
                    
        
        return set_k

l = [['кабачки', 'спаржа'],
     ['кабачки', 'фасоль'],
     ['капуста', 'перец'],
     ['кукуруза', 'помидоры'],
     ['кукуруза', 'фасоль'],
     ['помидоры', 'фасоль'],
     ['спаржа', 'фасоль']]
#print(get_n_common_elements (['кукуруза', 'помидоры'],['помидоры', 'фасоль']))


temp_for_check = merging_sets(['кукуруза', 'помидоры'],['помидоры', 'фасоль'],['помидоры'])

print("\nТройные",get_set_k(2,l))

l = [['кабачки', 'спаржа', 'фасоль'], ['кукуруза', 'помидоры', 'фасоль']]
#print(get_set_k(3,l))




k=1
frequent_sets = []
temp_set = frequent_one_set[:]
while True:
    frequent_sets.append(temp_set)
    #Находим к-предметные наборы и кладем их в frequent_sets
    temp_set = get_set_k(k,temp_set)
    k+=1
    if temp_set==[]: break

print("frequent_sets")  
for sets_k in frequent_sets:
    print(sets_k)
    print()  
    



#Принимает на вход набор и генерирует все возможные его поднаборы
def get_subsets(set):
    result_subsets = []
    n = len(set)-1
    while(n>=1):
        sub_temp = get_subs_size_count(set,n)
        for e in sub_temp:
            result_subsets.append(e)
        n-=1
    return [set,result_subsets]

#Принимает набор и количество елементов, которые должны быть в поднаборе
def get_subs_size_count(set, count):
    result =[]
    if count==1:
        for i in set:
             result.append(i)
    if count>=2:
        for i in range(len(set)-1):
            for j in range(i+1,len(set)):      
                result.append([set[i],set[j]])
    return result

#Ищем все элементы в set, которых нет в subset
def get_set_minus_sub(set,subset):
    res = []
    for s_el in set:
        if subset.count(s_el)==0 :
            res.append(s_el)
    return res
    
#Вернет поддержу для правила-кандидата
def get_support(set1,set2):
    count_of_trans = len(transaction_list)
    a_and_b_count = get_count_of_set_in_transaction(set1+set2)
    return a_and_b_count/count_of_trans

#Вернет достоверность для правила-кандидата
def get_credibility(set1,set2):
    a_count = get_count_of_set_in_transaction(set1)
    a_and_b_count = get_count_of_set_in_transaction(set1+set2)
    return a_and_b_count/a_count
    
#Принимает определенные элементы, тасует между собой, составляя кандидатов в правила, просчитывает для правила поддержку и достоверность
def associative_rule_candidates(set_and_subs):
    set = set_and_subs[0]
    subs = set_and_subs[1]
    candidates_for_rule = []
    
    for subs_el in subs:
        tmp_list = get_set_minus_sub(set,subs_el)
        if type(subs_el) is str: subs_el = [subs_el]
        candidates_for_rule.append([subs_el,tmp_list,0,0])
        
    #Нахождение поддержки и достоверности для всех кандидатов в правила
    for ind in range(len(candidates_for_rule)):
        #0-элемент это условие, 1- элемент это следствие, 2 - элемент это поддержка, 3 - элемент это достоверность
        candidates_for_rule[ind][2] = get_support(candidates_for_rule[ind][0],candidates_for_rule[ind][1])
        candidates_for_rule[ind][3] = get_credibility(candidates_for_rule[ind][0],candidates_for_rule[ind][1])
    return candidates_for_rule


associative_rule = []
#Генерация ассоциативных правил
#Начинаем рассматривать c двухэлементных наборов
for ind in range(1, len(frequent_sets)):
    subsets = []
    #Генерируем все возможные поднаборы s
    for set_k in frequent_sets[ind]:
        subsets_for_set=get_subsets(set_k)
        associative_rule += associative_rule_candidates(subsets_for_set)
for a in associative_rule:
    print(a)




