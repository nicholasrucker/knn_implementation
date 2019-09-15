import csv
import pandas as pd
import matplotlib.pyplot as plt
import math
import itertools

print("Enter a name for the input file:")
fileName = input()

predict = []
while True:
	print("Enter a value for body length and dorsal fin length: ")
	firstValue, secondValue = float(input()), float(input())
	
	if firstValue == 0 and secondValue == 0:
		break

	predict.append([firstValue, secondValue])

fileName = "FF74.txt"

# Here we are just converting the .txt to a .csv for easy retrieval of the data
with open(fileName, 'r') as inputFile:
    stripped = (line.replace('\t', ',').strip() for line in inputFile)
    lines = (line.split(',') for line in stripped if line)
    with open(fileName.replace(".txt", ".csv"), 'w') as outputFile:
        writer = csv.writer(outputFile)
        writer.writerows(lines)

inputFile.close()

# Now lets create the data frame and shuffle the data so our test/training splits are random 
fishDS = pd.read_csv(fileName.replace(".txt", ".csv"), header = None).dropna(inplace=False)
fishDS = fishDS.sample(frac=1).reset_index(drop=True)

# The map is going to have two keys: 0 and 1
# The values will be a list of pairs which represent the datapoints.
fishMap = {}

# Lets set up testing and training maps at the same time too
testingData = {}
trainingData = {}

# Since the data is randomized every time we run the program we can just take
# The first 20% of the values for testing and the rest for training

trainingObs = fishDS.shape[0] // 5


for index, row in fishDS.iterrows():
	if trainingObs > 0:
		if row[2] not in testingData.keys():
			testingData[row[2]] = [[row[0], row[1]]]
		else:
			testingData[row[2]].append([row[0], row[1]])
	else:
		if row[2] not in trainingData.keys():
			trainingData[row[2]] = [[row[0], row[1]]]
		else:
			trainingData[row[2]].append([row[0], row[1]])

	trainingObs -= 1

	if row[2] not in fishMap.keys():
		fishMap[row[2]] = [[row[0], row[1]]]
	else:
		fishMap[row[2]].append([row[0], row[1]])
	color = 'r'
	if row[2] == 1:
		color = 'k'
	plt.scatter(row[0], row[1], color = color)
#############################################plt.show()

def knn(train, test, k_neighbors):
	distances = []

	# We are just going to loop through to find all the distances between the points
	# Note this will only work for datasets with two features
	# I'll find a work around for that in a little bit
	for category in train:
		for dataPoint in train[category]:
			distance = math.sqrt((test[0] - dataPoint[0])**2 + (test[1] - dataPoint[1])**2)
			distances.append([distance, category])

	# We are throwing the decision logic into a loop in case there is a tie
	#while 1:
	# We need to sort the distances because we care about the nearest neighbors
	distances = sorted(distances)[:k_neighbors]

	# And really we just need the group so lets turn the list of lists into a flat list
	neighborList = []
	for item in distances:
		neighborList.append(item[1])
	
	cat0 = 0
	cat1 = 0

	for result in neighborList:
		if int(result) == 0:
			cat0 += 1
		else:
			cat1 += 1

	if cat1 > cat0:
		return 1
	elif cat0 > cat1:
		return 0
	else:
		# If there is a tie and we can add a neighbor, we do
		if len(train) - 3 > k_neighbors:
			k_neighbors += 1
		# If we cannot add a neighbor, we subtract one
		else:
			k_neighbors -= 1

# for item in predict:
# 	print(knn(fishMap, item, 3))
totalRight = 0
totalNumber = 0

for key, value in testingData.items():
	for result in value:
		predictedResult = knn(trainingData, result, 3)

		print("predicted was:", predictedResult)
		print("expected was:", int(key))
		print("             ")

		if predictedResult == int(key):
			totalRight += 1
		totalNumber += 1

print("Accuracy is:", totalRight/totalNumber)


