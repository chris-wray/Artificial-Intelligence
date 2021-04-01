import numpy
import random
import os
import matplotlib as plt

class data():
    def __init__(self, x, y, z, target):
        self.x = x
        self.y = y
        self.z = z
        self.target = target

    def print_data(self):
        print(str(self.x) + "\t" + str(self.y) + "\t" + str(self.z) + "\t:" + str(self.target))


class perceptron():
    bias = -1.0
    threshold = .5
    def __init__(self, learning_rate, num_inputs):
        self.learning_rate = learning_rate
        self.weights = []
        for i in range (0, num_inputs):
            self.weights.append(float(random.randrange(-2, 2)))
    
    def guess(self, inputs):
        sum = self.bias*self.threshold
        for i in range(0, len(inputs)):
            sum = sum + (inputs[i]*self.weights[i])
        if(sum > 0):
            return 1
        else:
            return 0
    
    def train(self, inputs, target):
        guess = self.guess(inputs)
        error  = target - guess
        if(error != 0):
            #print("Guessed " + str(guess) + " for inputs ", end="")
            #print(inputs)
            #print("Error is " + str(error))
            #print("Current weights: ", end="")
            #self.print_weights()
            self.threshold = self.threshold + (error*self.bias)
            for i in range (0, len(inputs)):
                self.weights[i] += (error*inputs[i])
                #print("\tWeight after: " + str(self.weights[i]))
            #print("Adjusted weights: ", end="")
            #self.print_weights()

    def print_weights(self):
        for weight in self.weights:
            print(str(weight), end=" ")
        print()


dataset = []

for i in range(0, 2):
    for j in range(0, 2):
        for k in range(0, 2):
            dataset.append(data(i, j, k, not(i and j and k)))

print("Test Data:")
for line in dataset:
    line.print_data()

p = perceptron(5, 3)

print("Untrained test:")
error = 0
for line in dataset:
    input = [line.x, line.y, line.z]
    guess = p.guess(input)
    #line.print_data()
    if(guess != line.target):
        error +=1
    #print(guess)
print("Untrained error: " + str(error))

print("Training data", end="")
while(error != 0):
    for line in dataset:
        input = [line.x, line.y, line.z]
        p.train(input, line.target)
        print(".", end="")
    
    error = 0
    for line in dataset:
        input = [line.x, line.y, line.z]
        guess = p.guess(input)
        #line.print_data()
        if(guess != line.target):
            error +=1
        #print(guess)
    #p.print_weights()
    print("Untrained error: " + str(error))
    #os.system("PAUSE")

print("Perceptron trained weights: ", end="")
p.print_weights()
print("Threshold: " + str(p.threshold))
