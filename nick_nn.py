import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
plt.show()


def knn(train, test, k_neighbors):
	for i in train:
		for j in train[i]:
			distance = sqrt((test[0] - j[0])**2 + (test[1] - j[1])**2)
	return results




