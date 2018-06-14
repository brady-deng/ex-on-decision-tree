from math import log
import operator

def calcEnt(dataset):
    num = len(dataset)
    labelcount = {}
    for featvec in dataset:
        currentlabel = featvec[-1]
        if currentlabel not in labelcount.keys():
            labelcount[currentlabel] = 0
        labelcount[currentlabel] += 1
    ent = 0.0
    for key in labelcount:
        prob = float(labelcount[key])/num
        ent -= prob*log(prob,2)
    return ent
def createdataset():
    dataset = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataset,labels
def splitdataset(dataset,axis,value):
    retdataset = []
    for featvec in dataset:
        if featvec[axis] == value:
            reducedfeatvec = featvec[:axis]
            reducedfeatvec.extend(featvec[axis+1:])
            retdataset.append(reducedfeatvec)
    return retdataset
def chooseBestFeatureTospilt(dataset):
    numFeatures = len(dataset[0]) - 1
    baseent = calcEnt(dataset)
    bestinfogain = 0.0;
    bestfea = -1
    for i in range(numFeatures):
        fealist = [example[i] for example in dataset]
        uniquevals = set(fealist)
        newent = 0.0
        for value in uniquevals:
            subdataset = splitdataset(dataset,i,value)
            prob = len(subdataset)/float(len(dataset))
            newent += prob*calcEnt(subdataset)
        infogain = baseent - newent
        if (infogain > bestinfogain):
            bestinfogain = infogain
            bestfea = i
    return bestfea
def majorityCnt(classList):
    classcount = {}
    for vote in classList:
        if vote not in classcount.keys(): classcount[vote] = 0
        classcount += 1
    sortedclasscount = sorted(classcount.items(),key = operator.itemgetter(1),reverse = True)
    return sortedclasscount[0][0]
def createTree(dataset,labels):
    classlist = [example [-1] for example in dataset]
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    if len(dataset[0]) == 1:
        return majorityCnt(classlist)
    bestfeat = chooseBestFeatureTospilt(dataset)
    bestlabel = labels[bestfeat]
    mytree = {bestlabel:{}}
    del(labels[bestfeat])
    featvalues = [example[bestfeat] for example in dataset]
    uniquevals = set(featvalues)
    for value in uniquevals:
        sublabels = labels[:]
        mytree[bestlabel][value] = createTree(splitdataset(dataset,bestfeat,value),sublabels)
    return mytree
def classify(inputtree,featlabel,testvec):
    firststr = list(inputtree.keys())[0]
    seconddict = inputtree[firststr]
    featindex = featlabel.index(firststr)
    for key in seconddict.keys():
        if testvec[featindex] == key:
            if type(seconddict[key]).__name__ == 'dict':
                classlabel = classify(seconddict[key],featlabel,testvec)
            else:
                classlabel = seconddict[key]
    return classlabel
def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                  ]
    return listOfTrees[i]
if __name__ == "__main__":
    dat,lab = createdataset()
    mytree = retrieveTree(0)
    print(classify(mytree,lab,[1,0]))
