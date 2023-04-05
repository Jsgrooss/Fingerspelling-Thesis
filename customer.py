import pygame
import dialogue
import random

mains = ["egg", "beef", "rice", "pork", "fish"]
drink = ["Tea", "coffee", "Water", "wine", "beer"]


class Customer():
    def __init__(self, name):
        self.name = name
        self.main = random.choice(mains)
        self.drink = random.choice(drink)

    def newOrder(self):
        self.main = random.choice(mains)
        self.drink = random.choice(drink)

    def askAbourOrder(self):
        return "My order was %s to eat and %s to drink" %(self.main,self.drink)
    


cust = Customer("Betty")