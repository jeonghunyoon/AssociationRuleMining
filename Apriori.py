# -*- coding: utf-8 -*-

### 1. item 1개의 list 를 원소로 가지는 candidate 을 구성한다.
def createC1(dataSet):
    candidate1 = []
    for data in dataSet:
        for item in data:
            if not [item] in candidate1:
                candidate1.append([item])
    candidate1.sort()
    return map(frozenset, candidate1)

### 2. 후보군으로 들어온 item list 에 대하여, dataSet을 scan하며 지지도(support)를 계산한다.
def scanDataSet(dataSet, candidateK, minSupport):
    supportCount = {}
    for data in dataSet:
        for items in candidateK:
            if items.issubset(data):
                if not supportCount.has_key(items): supportCount[items] = 1
                else:
                    supportCount[items] += 1
    nDataSet = float(len(dataSet))
    # 다음번(현재의 item들을 조합하여) 후보군을 생성하기 위하여 리스트를 생성
    retList = []
    supporOfItems = {}
    for key in supportCount:
        support = supportCount[key] / nDataSet
        if support >= minSupport:
            retList.insert(0, key)
        supporOfItems[key] = support
    return retList, supporOfItems