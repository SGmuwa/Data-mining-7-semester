#!/usr/bin/env python
# coding: utf-8

import pandas
import itertools

items = pandas.read_csv('transactions.txt', sep='\t')
for a in items['description'].unique(): print(a)
groupValues = items.groupby(by='description')

# Возвращает все комбинации условия и следствия.
def FindAllCombinations(hand, min = 1, max = None):
    if max == None: max = len(hand)
    max = max + 1
    Res = []
    for x in range(min, max):
        Res.extend(itertools.combinations(hand.groups.keys(), x))
    InverseRes = Res[:]
    InverseRes.reverse()
    return zip(Res, InverseRes)

for condition, effect in FindAllCombinations(groupValues, 1, len(groupValues) - 1):
    print(condition, effect)
