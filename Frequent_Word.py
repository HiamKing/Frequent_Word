#################################################
def getName(rawName):
    data = []
    strr = ""
    isName = 0
    for i in rawName:
        if i[len(i)-1] == ',' or i[len(i)-1] == '.':
            i = i[:len(i)-1]
        if i == "":
            continue
        if i[0] >= 'A' and i[0] <= 'Z':
            if isName == 0:
                strr = i
                isName = 1
            else:
                strr += " " + i
        else:
            if isName != 0:
                if strr not in data:
                    data.append(strr)
                isName = 0
                strr = ""
    return data

#################################################
def getData(firstDir):
    for i in range(1, 211):
        dirr = str(i)
        while len(dirr) < 3:
            dirr = "0" + dirr
        try:
            f = open(firstDir + dirr + ".txt", "r")
            pgh = f.read()
            rawName = pgh.split()
            data.append(getName(rawName))
        finally:
            f.close()

#################################################
def preProcess():
    getData("bbc\\business\\")
    getData("bbc\\entertainment\\")
    getData("bbc\\politics\\")
    getData("bbc\\sport\\")
    getData("bbc\\tech\\")

#################################################
def initData(data):
    uniqueItem = {}
    uniqueItem = set()
    for i in data:
        uniqueItem.update(i)
    
    return list(uniqueItem)
#################################################
def countOccurences(itemset, data):
    count = 0
    
    for i in range(len(data)):
        if set(itemset).issubset(set(data[i])):
            count += 1
    
    return count

#################################################
def getFrequent(itemsets, data, minSup, discarded):
    L = []
    supCount = []
    newDiscarded = []   
    numData = len(data)

    for s in range(len(itemsets)):
        discardBefore = False

        if len(discarded) > 0:
            for it in discarded:
                if set(it).issubset(set(itemsets[s])):
                    discardBefore = True
                    break

        if not discardBefore:
            count = countOccurences(itemsets[s], data)
            if count / numData > minSup:
                L.append(itemsets[s])
                supCount.append(count)
            else:
                newDiscarded.append(itemsets[s])
    return L, supCount, newDiscarded

#################################################
def jointTwoSet(set1, set2, uniqueItem):
    set1.sort( key=lambda x: uniqueItem.index(x))
    set2.sort( key=lambda x: uniqueItem.index(x))

    for i in range(len(set1) - 1):
        if set1[i] != set2[i]:
            return []
    
    if uniqueItem.index(set1[-1]) < uniqueItem.index(set2[-1]):
        return set1 + [set2[-1]]
    
    return []

#################################################
def joinItemSets(oldSet, uniqueItem):
    c = []
    for i in range(len(oldSet)):
        for j in range(i+1, len(oldSet)):
            newSet = jointTwoSet(oldSet[i], oldSet[j], uniqueItem)
            if len(newSet) > 0:
                c.append(newSet)
    
    return c

#################################################
def printFrequentName(frequentName, supCount, data):
    print("Name | Frequency")
    for i in range(len(frequentName)):
        print("{} : {}%".format(frequentName[i], supCount[i]/len(data)*100))

#################################################
data = []
print("[INFORMATION] Loading data...")
preProcess()
print("Please choose minsup:")
minSup = int(input())
minSup /= 100
c = {}
l = {}
discarded = {}
supCountL = {}
itemSize = 1
discarded.update({itemSize-1: []})
uniqueItem = initData(data)
c.update({itemSize : [ [f] for f in uniqueItem]})

for i in range(1, 3):
    itemSize = i
    f, sup , newDiscarded = getFrequent(c[itemSize], data, minSup, discarded[itemSize-1])
    discarded.update({itemSize: newDiscarded})
    l.update({itemSize: f})
    supCountL.update({itemSize: sup})
    c.update({itemSize+1: joinItemSets(l[itemSize], uniqueItem)})

printFrequentName(l[2], supCountL[2], data)


