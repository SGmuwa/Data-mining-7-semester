#!/usr/bin/env python
# coding: utf-8

import pandas
import itertools

items = pandas.read_csv('transactions.txt', sep='\t')
print(items['description'].unique())
groupValues = items.groupby(by='description').groups
for k, v in groupValues.items():
    toAdd = []
    for x in v:
        toAdd.append(items['id'][x])
    groupValues[k] = toAdd

def differenceDictionary(big, small):
    output = big.copy()
    for x in small.keys():
        if x in output.keys():
            del output[x]
    return output

def intersectionLists(list):
    intersection = None
    for v in list:
        if intersection == None:
            intersection = set(v)
            continue
        intersection &= set(v)
    return intersection

def dropImpossibleKeys(combinationsKeys):
    toRemove = []
    for i in range(len(combinationsKeys)):
        x = combinationsKeys[i]
        intersection = intersectionLists(x.values())
        if len(intersection) == 0:
            toRemove.append(i)
    toRemove.reverse()
    for i in toRemove:
        del combinationsKeys[i]

# Возвращает все комбинации условия и следствия.
def FindAllCombinations(hand, min = 1, max = None):
    if max == None: max = len(hand)
    max = max + 1
    Res = []
    combinationsKeys = []
    for x in range(min, max):
        buffer = list(itertools.combinations(hand, x))
        toAdd = []
        for y in range(len(buffer)):
            toAdd.append({})
            for z in buffer[y]:
                toAdd[y][z] = tuple(hand[z])
        combinationsKeys.extend(toAdd)
    dropImpossibleKeys(combinationsKeys)
    for x in combinationsKeys:
        withoutCondition = differenceDictionary(hand, x)
        effectCombinations = []
        for y in range(1, max - len(x)):
            effectCombinations.extend(itertools.combinations(withoutCondition, y))
        for y in range(len(effectCombinations)):
            for z in effectCombinations[y]:
                Res.append((x, {z: tuple(hand[z])}))
    return Res

rules = {}
for condition, effect in FindAllCombinations(groupValues, 1, len(groupValues) - 1):
    toIntersection = []
    needLen = 0
    for v in condition.values():
        toIntersection.append(v)
        needLen += len(v)
    for v in effect.values():
        toIntersection.append(v)
    intersection = intersectionLists(toIntersection)
    rules[(tuple(condition.items()), tuple(effect.items()))] = len(intersection) / needLen
for a in sorted(rules.items(), key=lambda kv: kv[1]):
    print(a)