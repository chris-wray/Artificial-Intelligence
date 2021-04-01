import math
import sys
import os

def entropy(a, b):
    #print("a: " + str(a) + " b: " + str(b) + " d: " + str(a+b))
    denominator = a+b
    pos = 0.0
    neg = 0.0
    if(a != 0):
        pos = -a/denominator * math.log(a/denominator, 2)
    #print("a piece: " + str(pos))
    if(b != 0):
        neg = -b/denominator * math.log(b/denominator, 2)
    #print("b piece: " + str(neg))

    #print("E: " + str(pos+neg))
    return neg+pos

class decision():

    def __init__(self, a, b):
        self.pos = a
        self.neg = b
        self.entropy = entropy(a, b)

    def print_decision(self):
        print("+: " + str(self.pos) + " -: " + str(self.neg) + " E: " + str(self.entropy))


class decision_tree():

    tree = []

    def __init__(self, s):
        #print("Making Tree")
        nums = []
        for i in range(0, len(s)):
            #print(s[i], end=" ")
            
            if(s[i].isnumeric()):
                #print(" is num")
                nums.append(float(s[i]))
            
            if (len(nums) == 2):
                #print("Appending")
                self.tree.append(decision(nums.pop(), nums.pop()))
        #print("Done making tree")

    def calculate_gain(self):
        sum = 0.0
        if self.tree:
            prior = self.tree.pop(0)
            print("Prior E: " + str(prior.entropy))
            for dec in self.tree:
                sum = sum + dec.entropy*(dec.pos+dec.neg)/(prior.pos+prior.neg)
            return prior.entropy-sum
        else:
            return 0
        
    def print_tree(self):
        for decision in self.tree:
            decision.print_decision()

def infogain(s):
    new_tree = decision_tree(s)
    #new_tree.print_tree()
    print("Information gain from " + s + " is " + str(new_tree.calculate_gain()))

statement = ""

for i in range(1, len(sys.argv)):
    statement = statement + str(sys.argv[i])

infogain(statement)


