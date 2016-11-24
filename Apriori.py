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


### 2. 후보군 candidate 생성. 예를 들어, {{1}, {2}, {3}}, k=2 가 input 으로 들어오면, {{1,2}, {2,3}, {1,3}} 이 생성될 것이다.
# TODO 나중에 좀 더 보자!!
def createCandidatesK(itemList, K):
    candidatesK = []
    nItems = len(itemList)

    for i in range(nItems):
        for j in range(i+1, nItems):
            # 두 item이 있을 때, 마지막 index를 제외하고 비교한다. 비교한 부분이 같다면, union 하면, 2 items의 끝부분이 union 된다.
            leftItem = list(itemList[i])[:K-2]
            rightItem = list(itemList[j])[:K-2]
            if leftItem == rightItem:
                candidatesK.append(itemList[i] | itemList[j])
    return candidatesK


### 3. 후보군으로 들어온 item list 에 대하여, dataSet을 scan하며 지지도(support)를 계산한다.
def scanDataSet(dataSet, kCandidate, minSupport):
    supportCount = {}
    for data in dataSet:
        for items in kCandidate:
            if items.issubset(data):
                if not supportCount.has_key(items): supportCount[items] = 1
                else:
                    supportCount[items] += 1
    nDataSet = float(len(dataSet))
    # 다음번(현재의 item들을 조합하여) 후보군을 생성하기 위하여 리스트를 생성
    itemList = []
    supportOfItems = {}
    for key in supportCount:
        support = supportCount[key] / nDataSet
        if support >= minSupport:
            itemList.insert(0, key)
            supportOfItems[key] = support
    return itemList, supportOfItems


### 4. 위의 method 를 조합하여, apriori 알고리즘을 수행한다.
def apriori(dataSet, minSupport = 0.5):
    candidates1 = createC1(dataSet)
    itemList1, supportOfItems = scanDataSet(dataSet, candidates1, minSupport)
    list = [itemList1]
    k = 2
    while (len(list[k-2]) > 0):
        candidatesK = createCandidatesK(list[k-2], k)
        itemListK, supportOfItemsK = scanDataSet(dataSet, candidatesK, minSupport)
        supportOfItems.update(supportOfItemsK)
        list.append(itemListK)
        k += 1
    return list, supportOfItems


### 5. 발생 빈도 수가 높은 아이템 freqItem 과 그것의 하위 집합이 input 으로 들어 갔을 때, 발생 가능 한 rule의 조합을 생성한다.
def ruleFromConseq(freqItem, subItem, supportData, result, minConf = 0.7):
    m = len(subItem[0])
    if (len(freqItem) > (m + 1)):
        # subItemCan 은, subItem 들을 조합하여, 아이템의 갯수가 1개 더 많은 candidate 를 만드는 것이다.
        targetItem = createCandidatesK(subItem, m + 1)
        # 먼저 confidence 를 계산부터 한다.
        targetItem = calcConf(freqItem, targetItem, supportData, result, minConf)
        # target item 의 갯수가 1인 것부터 시작해서 차츰 올라갈 것인데, 최소 신뢰도를 만족하는 것만 고려한다.
        if (len(targetItem) > 1):
            ruleFromConseq(freqItem, targetItem, supportData, result, minConf)


### 6. target : subItemCan 의 원소들, from : freqItem - subItemCan
def calcConf(freqItem, subItemCan, supportData, result, minConf):
    goodRules = []

    return goodRules