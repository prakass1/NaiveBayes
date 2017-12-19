import random 
import csv
import math
data=[]
def loadCsv(filename):
	with open('car.csv') as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		for row in csvReader:
			data.append(row)
	return data
def splitData(dataset,splitRatio):
	random.shuffle(dataset)
	print(len(dataset))
	trainSet=dataset[:(int)(len(dataset)*splitRatio)] 
	testSet=dataset[(int)(len(trainSet)):]
	return[trainSet,testSet]






def main():
	filename = 'car.csv'
	splitRatio = 0.75
	dataset = loadCsv(filename)
	trd,td=splitData(dataset, splitRatio)

	print(td)
	print(len(trd))
	print(len(td))

main()
 