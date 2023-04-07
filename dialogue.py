import pygame
import string
from copy import deepcopy
from enum import Enum

#chr(ord('@') + 1) -> A

class DialogueNodeType(Enum):
    Linear = 1
    Multi = 2
    PlayerInput = 3

class Dialogue():
    def __init__ (self, x, y, nodeType, text, font, text_color, scene, character, next):
        self.x = x
        self.y = y
        self.type = DialogueNodeType(nodeType)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.scene = scene
        self.character = character
        self.next = next
        self.img = font.render(text, True, text_color)
    
    def draw_text(self, surface, debug):
        pass

    def progress_dialogue(self):
        pass


def insertDialogue(dialogue1:Dialogue, dialogue2:Dialogue, newDialogue:Dialogue):
    newDia = newDialogue
    dialogue1.next = newDia
    newDia.next = dialogue2

class LinearDialogueNode(Dialogue):
    def __init__ (self, x, y, nodeType, text, font, text_color, scene, character, next):
        self.x = x
        self.y = y
        self.type = DialogueNodeType(nodeType)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.scene = scene
        self.character = character
        self.next = next
        self.img = font.render(text, True, text_color)


    def draw_text(self, surface, debug):
        if debug:
            self.img = self.font.render(self.character + ": " + self.text, True, self.text_color)
            surface.blit(self.img, (self.x - self.img.get_width()/2, self.y))
        else:
            surface.blit(self.img, (self.x - self.img.get_width()/2, self.y))    

    def progress_dialogue(self):
        return self.next


class MultiDialogueNode(Dialogue):
    def __init__ (self, x, y, nodeType, text, font, text_color, scene, character, choices, next_dialogues):
        self.x = x
        self.y = y
        self.type = DialogueNodeType(nodeType)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.scene = scene
        self.character = character
        self.choices = choices
        self.next_dialogues = next_dialogues
        self.img = font.render(text, True, text_color)

    def draw_text(self, surface, debug):
        if debug:
            self.img = self.font.render(self.character + ": " + self.text, True, self.text_color)
            surface.blit(self.img, (self.x - self.img.get_width()/2, self.y))
        else:
            surface.blit(self.img, (self.x - self.img.get_width()/2, self.y))    

    def progress_dialogue(self, choice):
        if choice == 1:
            return self.next_dialogues[0]
        if choice == 2:
            return self.next_dialogues[1]
        if choice == 3:
            return self.next_dialogues[2]
        
        
class PlayerInputDialogue(Dialogue):
    def __init__ (self, x, y, nodeType, text, font, text_color, scene, character, letters, next):
        self.x = x
        self.y = y
        self.type = DialogueNodeType(nodeType)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.scene = scene
        self.character = character
        self.letters = letters
        self.next = next
        self.img = font.render(text, True, text_color)


    def draw_text(self, surface, debug):
        if (len(self.letters) == 1):
            letterNumber = string.ascii_uppercase.index(self.letters)
            letterImg = pygame.image.load("LetterPictures/"+str(letterNumber)+".png").convert_alpha()
            if debug:
                self.img = self.font.render(self.character + ": " + self.text, True, self.text_color)
                surface.blit(self.img, (self.x - self.img.get_width()/2, self.y))
                surface.blit(letterImg,((self.x - self.img.get_width()/2, self.y-100)))
            else:
                surface.blit(self.img, (self.x - self.img.get_width()/2, self.y))
                surface.blit(letterImg,((self.x - self.img.get_width()/2, self.y-100)))    
        else:
            count = 0
            for l in self.letters:
                print(l)
                lNumber = string.ascii_uppercase.index(l)
                letterImg = pygame.image.load("LetterPictures/"+str(lNumber)+".png").convert_alpha()
                surface.blit(letterImg,((self.x - self.img.get_width()/2 + letterImg.get_width() * count, self.y-100)))
                count += 1
            
            self.img = self.font.render(self.character + ": " + self.text, True, self.text_color)
            surface.blit(self.img, (self.x - self.img.get_width()/2, self.y))

    def progress_dialogue(self):
        return self.next