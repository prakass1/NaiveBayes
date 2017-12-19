import random 
import csv
import math
from decimal import Decimal
data=[]

def loadCsv(filename):
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            data.append(row)
    return data

def calcPriorProbablity(priorProbCounts,trainingData):
    length = len(trainingData[0]) -1
    for val in trainingData:
        if not val[length] in priorProbCounts:
            print("Entered")
            priorProbCounts[val[length]] = 0
        else:
            #values = priorProb[val[6]]
            priorProbCounts[val[length]] = priorProbCounts.get(val[length]) + 1
            
    return priorProbCounts

def splitData(dataset,splitRatio):
    #random.shuffle(dataset)
    #print(len(dataset))
    trainSet=dataset[:(int)(len(dataset)*splitRatio)] 
    testSet=dataset[(int)(len(trainSet)):]
    return[trainSet,testSet]
    
def priorProb(classification,length):
    priorProbablity = {}
    for i in classification:
        priorProbablity[i]= classification[i]/length
        
        
    return priorProbablity

def main():
    filename = 'car.csv' 
    splitRatio = 0.75
    dataset = loadCsv(filename)
    trainingData,testData = splitData(dataset, splitRatio)
    
    target='class'
    attributes = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
    
    print(trainingData[0])
    priorProbCounts = {}
    priorProbCounts = calcPriorProbablity(priorProbCounts,trainingData)
    priorProbablity = priorProb(priorProbCounts,len(trainingData))
    print(len(trainingData))
    print(len(testData))
    print(priorProbCounts)
    print(priorProbablity)
main()
