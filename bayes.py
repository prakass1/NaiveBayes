import random 
import csv
import math
data=[]
def loadCsv(filename):
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            data.append(row)
    return data


def splitData(dataset,splitRatio):
    random.shuffle(dataset)
    #print(len(dataset))
    trainSet=dataset[:(int)(len(dataset)*splitRatio)] 
    testSet=dataset[(int)(len(trainSet)):]
    return[trainSet,testSet]

def main():
    filename = 'car.csv'
    splitRatio = 0.75
    dataset = loadCsv(filename)
    trainingData,testData = splitData(dataset, splitRatio)
    
    print(len(trainingData))
    print(len(testData))

main()
