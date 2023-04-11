import pygame
import dialogue
import random

pygame.init()

mains = ["egg", "beef", "rice", "pork", "fish"]
drink = ["Tea", "coffee", "Water", "wine", "beer"]


font = pygame.font.SysFont("arialblack", 40)
BLACK = (255,255,255)

class Customer():
    def __init__(self, name, w, h):
        self.name = name
        self.main = random.choice(mains)
        self.drink = random.choice(drink)
        self.w = w
        self.h = h

    def newOrder(self):
        self.main = random.choice(mains)
        self.drink = random.choice(drink)

        newCustDialogue = dialogue.CustomerDialogue(self.w/2, self.h/2, 4, "I would like %s to eat and %s to drink"  %(self.main,self.drink),
                                                    font, BLACK, "customer", "customer", [self.main, self.drink], None)

        return newCustDialogue

    def askAbourOrder(self):
        return "My order was %s to eat and %s to drink" %(self.main,self.drink)