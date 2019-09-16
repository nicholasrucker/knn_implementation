import csv
import pandas as pd
import matplotlib.pyplot as plt
import math
import itertools

print("\nEnter a name for the input file:")
fileName = input()

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

# Lets normalize the data (Only columns 0 and 1 since 2 has our classification)
cols_to_norm = [0,1]

# First lets store the information to we can normalize data the user enters via command line later
col0Mean = fishDS[0].mean()
col1Mean = fishDS[1].mean()

col0STD = fishDS[0].std()
col1STD = fishDS[1].std()

fishDS[cols_to_norm] = fishDS[cols_to_norm].apply(lambda x: (x - x.mean()) / x.std())

# The map is going to have two keys: 0 and 1
# The values will be a list of pairs which represent the datapoints.
fishMap = {}

# Lets set up testing and training maps at the same time too
testingData = {}
trainingData = {}

# Since the data is randomized every time we run the program we can just take
# The first 20% of the values for testing and the rest for training

trainingObs = fishDS.shape[0] // 5

# We will divide the current body and dorsil length by the max to standardize the data (0, 1]
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

#####################################################
# Un-comment this block if you would like to see a plot of the raw data
# (The data that becomes the training data)
	if row[2] not in fishMap.keys():
		fishMap[row[2]] = [[row[0], row[1]]]
	else:
		fishMap[row[2]].append([row[0], row[1]])
# 	color = 'r'
# 	if row[2] == 1:
# 		color = 'k'
# 	plt.scatter(row[0], row[1], color = color)
# plt.show()
#####################################################

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
	while 1:
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
			return '1'
		elif cat0 > cat1:
			return '0'
		else:
			# If there is a tie and we can add a neighbor, we do
			if len(train) - 3 > k_neighbors:
				k_neighbors += 1
			# If we cannot add a neighbor, we subtract one
			else:
				k_neighbors -= 1

# Now lets see our accuracy with 1 to 10 neighbors
# for i in range(1,22,2):
# 	totalRight = 0
# 	totalNumber = 0
# 	falsePositives = 0
# 	falseNegatives = 0
# 	for key, value in testingData.items():
# 		for result in value:
# 			predictedResult = knn(trainingData, result, i)

# 			if predictedResult == int(key):
# 				totalRight += 1
# 			totalNumber += 1

# 	print("K is:", i,"Total incorrect =", totalNumber - totalRight)
# 	print(totalNumber)

while 1:
	predict = []
	print("\nEnter a value for body length and dorsal fin length (press enter after each entry): ")
	firstValue, secondValue = float(input()), float(input())
	
	if firstValue == 0 and secondValue == 0:
		break

	predict.append([(firstValue - col0Mean) / col0STD, (secondValue - col1Mean) / col1STD])

	print("Predicted: TigerFish" + knn(fishMap, predict[0], 9))
