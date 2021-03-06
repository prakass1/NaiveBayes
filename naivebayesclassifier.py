import random
import csv

'''
A implementation of a Naive Bayesian Classifier using car dataset

    File name: naivebayesclassifier.py
    Team Members: 
        Nikhil Murthy (220641)
        Rutuja Pawar (220051)
        Subash Prakash (220408)
    Usage:
    To run the program, copy the input csv data file (car.data) in the same directory as the 
    program file, and issue the command "python naivebayesclassifier.py".
    
    Environment Tested:
    PYTHON : 3.6

'''

data = []
#getting the csv file and converting each row into a unit in a list
def loadCsv(filename):
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            data.append(row)
    return data

##calculating the probability of each target value
def calcPriorProbablity(priorProbCounts, trainingData, classIndex):
    for val in trainingData:
        if not val[classIndex] in priorProbCounts:
            priorProbCounts[val[classIndex]] = 1
        else:
            priorProbCounts[val[classIndex]] = priorProbCounts.get(val[classIndex]) + 1
    return priorProbCounts

#split the data into 2/3rd of its total to training and testSet
def splitData(dataset, splitRatio):
    random.shuffle(dataset)
    trainSet = dataset[:(int)(len(dataset) * splitRatio)]
    testSet = dataset[(int)(len(trainSet)):]
    return [trainSet, testSet]

#calculating Prior probabilite of each class
def priorProb(priorProbablity, classification, length):
    for key, val in classification.items():
        #print("Key --" + str(key) + "and Value --" + str(val))
        priorProbablity[key] = (val / length)
    return priorProbablity

# Check each of the attr and get the count of them as the attr
def calcAttrCount(trainingData, count):
    attrsProbCounts = {}
    for val in trainingData:
        if val[6] not in attrsProbCounts:
            attrsProbCounts[val[6]] = {}

        if val[count] not in attrsProbCounts[val[6]]:
            attrsProbCounts[val[6]][val[count]] = 1

        else:
            attrsProbCounts[val[6]][val[count]] = attrsProbCounts.get(val[6], {}).get(val[count]) + 1

    return attrsProbCounts

#classify of test data based on the  probability
def classify(buyingProbablity, maintProbablity, doorsProbablity, personsProbablity, lugBootProbablity, safetyProb,
             priorProbablity, testItem):
    bestF = float(-1)
    best = None
    #calculating Bayesian classifier based on individual probabilities
    for key in priorProbablity.keys():
        #Returns a default 0 if probablity not present
        pBuying = buyingProbablity.get(key).get(testItem[0], 0.0)

        pMaint = maintProbablity.get(key).get(testItem[1], 0.0)

        pDoors = doorsProbablity.get(key).get(testItem[2], 0.0)

        pPersons = personsProbablity.get(key).get(testItem[3], 0.0)

        pLugBoot = lugBootProbablity.get(key).get(testItem[4], 0.0)

        pSafety = safetyProb.get(key).get(testItem[5], 0.0)

        pPrior = priorProbablity.get(key)

        p = pPrior * pBuying * pMaint * pDoors * pPersons * pLugBoot * pSafety

        if (p > bestF):
            bestF = p
            best = key
    return best


def calcAttrProbablity(target, val, count):
    for key, value in val.items():
        value = (value) / (count)
        val[key] = value


def testDataItem(buyingProbablity, maintProbablity, doorsProbablity, personsProbablity, lugBootProbablity, safetyProb,
                 priorProbablity, testData):
    fail = 0.0
    for val in testData:
        if ((
        classify(buyingProbablity, maintProbablity, doorsProbablity, personsProbablity, lugBootProbablity, safetyProb,
                 priorProbablity, val)) != val[6]):
            fail = fail + 1


    #returning the fail probability
    return float((fail / len(testData)))


#This prepares to print a confusion matrix
def outMatrix(matrix,temp):
    for key in matrix.keys():
        key=key.split(",")
    header=""
    row=""
    for i in range(0,len(temp)):
        header=header+"\t"+temp[i]
        row=row+str(temp[i])
        for j in range(0,len(temp)):

            f=temp[i]+","+temp[j]
            if f in matrix.keys():

                row = row + "\t" + str(matrix[f])
            else:
                row = row+ "\t" + "."

        row = row+'\n'
    print(header)
    print(row)


#genarating the confusion matrix
def confusionMatrix(testData,buyingProbablity, maintProbablity, doorsProbablity, personsProbablity, lugBootProbablity, safetyProb,
                 priorProbablity):

    actual = []
    matrix={}
    predicted = []
    temp=[]
    for item in testData:
        predClass = classify(buyingProbablity, maintProbablity, doorsProbablity, personsProbablity, lugBootProbablity, safetyProb, priorProbablity, item)
        predicted.append(predClass)
        actual.append(item[6])
        #Of the form actual --> pred
        key = item[6]+ ","+predClass
        if predClass not in temp:
            temp.append(predClass)
            
        #Building a Structure for the count.
        if key not in matrix:
            matrix[key] = 1

        else:
            matrix[key] = matrix.get(key) + 1

    return outMatrix(matrix,temp)


################
#Start of main
################
def main():
    filename = 'car.csv'
    splitRatio = float(2/3)
    dataset = loadCsv(filename)
    target = 'class'
    attributes = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
    classIndex = attributes.index(target)
    summ_err = 0.0
    mean = 0.0
    K=100

    for k in range(0, K):
        trainingData, testData = splitData(dataset, splitRatio)

        #print(len(testData))
        file = open('out.csv', 'w')

        for val in trainingData:
            file.write(str(val) + "\n")
        buyingProbablity = {}
        maintProbablity = {}
        doorsProbablity = {}
        personsProbablity = {}
        lugBootProbablity = {}
        priorProbCounts = {}
        priorProbablity = {}
        safetyProb = {}

        calcPriorProbablity(priorProbCounts, trainingData, classIndex)
    
        priorProb(priorProbablity, priorProbCounts, len(trainingData))
        #Go through the attributes and fetch the probablities
        for attribute in attributes:
            #attrCounts = calcAttrCount(trainingData, attributes.index(attribute))

            if (attribute == 'buying'):
                buyingProbablity = calcAttrCount(trainingData, attributes.index(attribute))

            if (attribute == 'maint'):
                maintProbablity = calcAttrCount(trainingData, attributes.index(attribute))

            if (attribute == 'doors'):
                doorsProbablity = calcAttrCount(trainingData, attributes.index(attribute))

            if (attribute == 'persons'):
                personsProbablity = calcAttrCount(trainingData, attributes.index(attribute))

            if (attribute == 'lug_boot'):
                lugBootProbablity = calcAttrCount(trainingData, attributes.index(attribute))

            if (attribute == 'safety'):
                safetyProb = calcAttrCount(trainingData, attributes.index(attribute))

        # Calculating all probability and adding to dictionary
        for targetClass, count in priorProbCounts.items():
            calcAttrProbablity(targetClass, buyingProbablity.get(targetClass), count)
            calcAttrProbablity(targetClass, maintProbablity.get(targetClass), count)
            calcAttrProbablity(targetClass, doorsProbablity.get(targetClass), count)
            calcAttrProbablity(targetClass, personsProbablity.get(targetClass), count)
            calcAttrProbablity(targetClass, lugBootProbablity.get(targetClass), count)
            calcAttrProbablity(targetClass, safetyProb.get(targetClass), count)

        #getting the number of misclassification
        fail = testDataItem(buyingProbablity, maintProbablity, doorsProbablity, personsProbablity, lugBootProbablity,
                            safetyProb, priorProbablity, testData)

        summ_err = summ_err + fail


        #Calculating the mean average of errors for last five runs
        if(k>=95):
            mean = mean+summ_err
            
        #Printing the confusion matrix on the last run
        if(k==99):
            print("Printing Confusion Matrix")
            confusionMatrix(testData,buyingProbablity, maintProbablity, doorsProbablity, personsProbablity, lugBootProbablity,safetyProb, priorProbablity)

    print("Percentage of errors for the 100 runs " + str((summ_err / 100) * 100))
    print("average errors of the last five results is: " +str(mean/5) )

main()
