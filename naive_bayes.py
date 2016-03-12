import csv
import random
import math
import numpy

def loadCsv(filename):
	lines = csv.reader(open(filename , "rb"))
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset

def splitdata(dataset , ratio):
	training = []
	test = dataset
	count = int(ratio * len(dataset))
	i = 0
	while i < count:
		r = random.random()
		r *= len(test)
		index = int(r)
		training.append(test.pop(index))
		i = i + 1
	return [training , test]

def seperateClasses(dataset):
	seperated = {}
	for i in range(len(dataset)):
		if len(dataset[i]) == 0:
			continue
		class_data_item = int(dataset[i][-1])
		# print "class " , class_data_item
		if class_data_item not in seperated:
			seperated[class_data_item] = []
		seperated[class_data_item].append(dataset[i])
	# print seperated[0]
	# print "next class"
	# print seperated[1]
	return seperated

def mean(numbers):
	return numpy.sum(numbers)/float(len(numbers))

def stdev(numbers):
	average = mean(numbers)
	A = [(x - average)*(x - average) for x in numbers]
	variance = numpy.sum(A)
	if len(A) > 1:
		variance /= float(len(A) - 1)
	# print "variance " , math.sqrt(variance)
	return math.sqrt(variance)

def summarize(dataset):
	summary = []
	for j in range(len(dataset[0])):
		A = []
		for i in range(len(dataset)):
			A.append(dataset[i][j])
		# print sum(A)
		summary.append([mean(A) , stdev(A)])
	# print summary
	return summary


def calculateProbability(x , mean , stdev):
	if stdev == 0 or stdev + mean == 0:
		return 1
	power = (x - mean) * (x - mean)
	power /= float(2 * stdev * stdev)
	# print "power " , power
	if power > 50:
		return pow(1,-20)
	den = long(math.exp(power))
	den *= stdev * math.sqrt(2 * math.pi)
	return 1 / den

def classProbability(summary , data):
	prob = 1.0
	for i in range(len(data)):
		mean = summary[i][0]
		stdev = summary[i][1]
		# print "value {0} mean {1}",data[i],mean
		prob *= calculateProbability(data[i] , mean , stdev)
	return prob

def predictClass(summary , data):
	prob = 0
	predictedClass = 0
	for i in range(len(summary)):
		# print "class " , i
		classProb = classProbability(summary[i] , data)
		# print classProb
		if classProb > prob:
			prob = classProb
			predictedClass = i
	return predictedClass

filename = 'small-pima-indians.data.csv'
dataset = loadCsv(filename)
print('Loaded data file {0} with {1} rows').format(filename, len(dataset))
ratio = 0.67
training , test = splitdata(dataset , ratio)

# print "split data"
# print len(training)
# print training
# print len(test)
# print test

#split the training data set according to class
seperated = seperateClasses(training)

# print "seperation"
# print seperated[0]
# print seperated[1]
# print len(seperated[0]) + len(seperated[1])

classes = 2		#total number of classes in dataset
summary = {}
for i in range(classes):
	if i in seperated:
		summary[i] = summarize(seperated[i])
		# print len(summary[i])

#summary[i][j] denote mean and variance of jth attribute of ith class

# print summary[0][0]


# print "testing mean and variance"
# numbers = [1,2,3,4,5]
# print mean(numbers)
# print stdev(numbers)
# print calculateProbability(71.5 , 73 , 6.2)
# print classProbability(summary[0] , test[0])
# print predictClass(summary , test[0])

correct = 0
for i in range(len(test)):
	data = test[i]
	# print data
	if len(data) == 0:
		print "empty " , data
		continue
	v1 = int(data[-1])
	v2 = int(predictClass(summary , data))
	# print v1 , v2
	if v1 == v2:
		correct = correct + 1

print "correct " , correct

print "accuracy"
print (float(correct) / float(len(test))) * 100

# for i in range(10):
# 	print len(dataset[i])
# 	print dataset[i][0]