import pygame
import button
import dialogue
import string
import gestureRecognizer

pygame.init()

#TODO SECTION
# 1: create dector for full words ....Done?....
# 2: Make it so the dector doesn't have to reinitialize every time
# 3: Customer orders
# 4: Place things in correct places
# 5: replace imagedisplayer number in gesture recognizer with local variable
# 6: Allow game to be paused during detection

#Create game window
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

recognizer = gestureRecognizer.GestureRecognizer("eng")

#game variables
game_paused = True 
clicked = False
progressed_dialogue = False
waiting_for_input = False
menu_state = "main"
level_state = ""
scene_state = ""
current_dialogue = None

#Define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colors
BLACK = (255,255,255)
WHITE = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#load button images
play_img = pygame.image.load("images/button_play.png").convert_alpha()
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load("images/button_video.png").convert_alpha()
audio_img = pygame.image.load("images/button_audio.png").convert_alpha()
keys_img = pygame.image.load("images/button_keys.png").convert_alpha()
back_img = pygame.image.load("images/button_back.png").convert_alpha()
introduction_img = pygame.image.load("images/button_introduction.png").convert_alpha()
lvl1_img = pygame.image.load("images/button_level1.png").convert_alpha()
lvl2_img = pygame.image.load("images/button_level2.png").convert_alpha()

#Dialogue

#Testing for single character detection

sixth_dialogue = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 3, "Now this is the letter E", font, BLACK, "kitchen", "chef", "E", None)
fifth_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 1, "Very good!", font, BLACK, "kitchen", "chef", sixth_dialogue)
fourth_dialogue = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 3, "I am the chef, this is the ltter A", font, BLACK, "kitchen", "chef", "A", fifth_dialogue)
third_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 1, "This is the chef", font, BLACK, "kitchen", "manager", fourth_dialogue)
second_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 1, "Blah, blah, Ill show you to the chef", font, BLACK, "front", "manager", third_dialogue)
first_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 1, "Hello and welcome to the restaurant", font, BLACK, "front",  "manager", second_dialogue)
#test_word_input = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 3, "This is how you spell tea", font, BLACK, "kitchen", "chef", "TEA", fifth_dialogue)
#test_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 1, "TESTTESTTEST", font, BLACK, "front",  "manager", None)



#main menu
play_button = button.Button(SCREEN_WIDTH/2 - play_img.get_width()/2, 125, play_img, 1)

#general buttons
resume_button = button.Button(SCREEN_WIDTH/2 - resume_img.get_width()/2, 125, resume_img, 1)
options_button = button.Button(SCREEN_WIDTH/2 - options_img.get_width()/2, 250, options_img, 1)
quit_button = button.Button(SCREEN_WIDTH/2 - quit_img.get_width()/2, 375, quit_img, 1)

#options menu
video_button = button.Button(SCREEN_WIDTH/2 - video_img.get_width()/2, 75, video_img, 1)
audio_button = button.Button(SCREEN_WIDTH/2 - audio_img.get_width()/2, 200, audio_img, 1)
keys_button = button.Button(SCREEN_WIDTH/2 - keys_img.get_width()/2, 325, keys_img, 1)
back_button = button.Button(SCREEN_WIDTH/2 - back_img.get_width()/2, 450, back_img, 1)

#level menu
introduction_button = button.Button(SCREEN_WIDTH/2 - introduction_img.get_width()/2, 150, introduction_img, 1)
lvl1_button = button.Button(SCREEN_WIDTH/2 - lvl1_img.get_width()/2, 250, lvl1_img, 1)
lvl2_button = button.Button(SCREEN_WIDTH/2 - lvl2_img.get_width()/2, 350, lvl2_img, 1)

#Helper functions
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x-img.get_width()/2,y))

def checkDialogue():
    global current_dialogue
    global level_state
    global scene_state
    global menu_state
    global game_paused
    global waiting_for_input
    if current_dialogue.progress_dialogue() is not None:
        current_dialogue = current_dialogue.progress_dialogue()
    else:
        print("final dialogue of this chapter, return to menu")
        level_state = ""
        scene_state = ""
        menu_state = "main"
        game_paused = True
        waiting_for_input = False
        current_dialogue = None

#clean when created
user_text = ""

#game loop
run = True

while run:

    #fill according to scene
    if scene_state == "":
        screen.fill((58,78,91))
        draw_text("In Menu", font, BLACK, SCREEN_WIDTH/2, SCREEN_HEIGHT/4 - SCREEN_HEIGHT/4)
    if scene_state == "front":
        screen.fill((150,78,91))
        draw_text("In front of house", font, BLACK, SCREEN_WIDTH/2, SCREEN_HEIGHT/4 - SCREEN_HEIGHT/4)
    if scene_state == "kitchen":
        screen.fill((0,78,91))
        draw_text("In the kitchen", font, BLACK, SCREEN_WIDTH/2, SCREEN_HEIGHT/4 - SCREEN_HEIGHT/4)
    if scene_state == "customer":
        screen.fill((91,91,91))
        draw_text("With customer", font, BLACK, SCREEN_WIDTH/2, SCREEN_HEIGHT/4 - SCREEN_HEIGHT/4)

    #check if game is pause
    if game_paused == True: 
        #check menu state
        if menu_state == "main":
            if play_button.draw(screen) and clicked == False:
                menu_state = "level"
                clicked = True
            if options_button.draw(screen) and clicked == False:
                menu_state = "options"
                clicked = True
            if quit_button.draw(screen):
                run = False
        if menu_state == "pause":
            #draw pause screen buttons
            if resume_button.draw(screen) and clicked == False:
                game_paused = False
                clicked = True
            if options_button.draw(screen) and clicked == False:
                menu_state = "options"
                clicked = True
            if quit_button.draw(screen) and clicked == False:
                run = False
                clicked = True
        if menu_state == "options":
            if video_button.draw(screen) and clicked == False:
                clicked = True
                pass
            if audio_button.draw(screen) and clicked == False:
                clicked = True
                pass
            if keys_button.draw(screen) and clicked == False:
                clicked = True
                pass
            if back_button.draw(screen) and clicked == False:
                menu_state = "main"
                clicked = True
        if menu_state == "level":
            if introduction_button.draw(screen) and clicked == False:
                level_state = "introduction"
                current_dialogue = first_dialogue
                clicked = True
                game_paused = False
            if lvl1_button.draw(screen) and clicked == False:
                level_state = "lvl1"
                clicked = True
                game_paused = False
            if lvl2_button.draw(screen) and clicked == False:
                level_state = "lvl2"
                clicked = True
                game_paused = False
            if back_button.draw(screen) and clicked == False:
                menu_state = "main"
                clicked = True
    else:
        if level_state == "introduction":
            current_dialogue.draw_text(screen, True)
            scene_state = current_dialogue.scene
            if current_dialogue.type == dialogue.DialogueNodeType(3):
                #current_dialogue.draw_text(screen, True)
                waiting_for_input = True
        if level_state == "lvl1":
            draw_text("Welcome to level 1", font, BLACK, 100, 250)
        if level_state == "lvl2":
            draw_text("Welcome to levesl 2", font, BLACK, 100, 250)

    #TODO create a detection for full words
    if waiting_for_input == True:
        if (len(current_dialogue.letters) == 1):
            if recognizer.detectLetter(screen, SCREEN_WIDTH, SCREEN_HEIGHT, current_dialogue.letters):
                waiting_for_input = False        
                checkDialogue()
        else:
            if recognizer.detectWord(screen, SCREEN_WIDTH, SCREEN_HEIGHT, current_dialogue.letters):
                waiting_for_input = False        
                checkDialogue()

    #TODO
    #needs to be cleaned up
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = True
                menu_state = "pause"
            if event.key == pygame.K_SPACE and progressed_dialogue == False and waiting_for_input == False and game_paused == False:
                progressed_dialogue = True
                print(current_dialogue)
                checkDialogue()

            #Handle player keyboard input
            if(event.key == pygame.K_BACKSPACE and waiting_for_input == True):
                user_text = user_text[0:-1]
            elif(event.key == pygame.K_RETURN and waiting_for_input == True):
                guess = string.ascii_uppercase.index(user_text[0].upper())
                if(guess == current_dialogue.letter):
                    user_text = ""
                    waiting_for_input = False
                    checkDialogue()
            else:
                user_text = event.unicode

        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and progressed_dialogue == True:
                progressed_dialogue = False
                print("ready to progress")

    pygame.display.update()


pygame.quit() 