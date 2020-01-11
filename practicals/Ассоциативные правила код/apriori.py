#!/usr/bin/env python
# coding: utf-8

import pandas
import itertools

items = pandas.read_csv('transactions.txt', sep='\t')
for a in items['description'].unique(): print(a)
groupValues = items.groupby(by='description').groups

def differenceDictionary(big, small):
    output = big.copy()
    for x in small.keys():
        if x in output.keys():
            del output[x]
    return output

# Возвращает все комбинации условия и следствия.
def FindAllCombinations(hand, min = 1, max = None):
    if max == None: max = len(hand)
    max = max + 1
    Res = {}
    combinationsKeys = []
    for x in range(min, max):
        buffer = list(itertools.combinations(hand, x))
        toAdd = []
        for y in range(len(buffer)):
            toAdd.append({})
            for z in buffer[y]:
                toAdd[y][z] = tuple(hand[z])
        combinationsKeys.extend(toAdd)
    print(combinationsKeys[0])
    for x in combinationsKeys:
        withoutCondition = differenceDictionary(hand, x)
        effectCombinations = []
        for y in range(1, max - len(x)):
            effectCombinations.extend(itertools.combinations(withoutCondition, y))
        toAdd = []
        for y in range(len(effectCombinations)):
            toAdd.append({})
            for z in effectCombinations[y]:
                toAdd[y][z] = tuple(hand[z])
        Res[frozenset(x.items())] = toAdd
    return Res

for condition, effect in FindAllCombinations(groupValues, 1, len(groupValues) - 1).items():
    print(condition, effect)
    input()
    