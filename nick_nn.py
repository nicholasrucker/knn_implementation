import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from collections import Counter

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

for index, row in fishDS.iterrows():
	if row[2] not in fishMap.keys():
		fishMap[row[2]] = [[row[0], row[1]]]
	else:
		fishMap[row[2]].append([row[0], row[1]])
	color = 'r'
	if row[2] == 1:
		color = 'k'
	plt.scatter(row[0], row[1], color = color)
#plt.show()

predict = [80, 7]

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
		neighborList = [item for sublist in distances for item in sublist]
		
		cat0 = 0
		cat1 = 0

		for result in neighborList:
			if result == 0:
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


print(knn(fishMap, predict, 3))




