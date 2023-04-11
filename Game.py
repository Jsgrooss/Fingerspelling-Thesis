import pygame
import button
import dialogue
import string
import gestureRecognizer
import game_customer

pygame.init()

#TODO SECTION
# 1: create dector for full words ....Done?....
# 2: Make it so the dector doesn't have to reinitialize every time ...Done...
# 2.1 : Camera still has to reinitialize, can possibly be fixed
# 3: Customer orders
# 4: Place things in correct places
# 5: replace imagedisplayer number in gesture recognizer with local variable
# 6: Allow game to be paused during detection
# 7: Give feedback on accepted letter

#Create game window
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#Stuff
recognizer = gestureRecognizer.GestureRecognizer("eng")
g_customer = game_customer.Customer("TestName", SCREEN_HEIGHT, SCREEN_WIDTH)

#game variables
game_paused = True 
clicked = False
progressed_dialogue = False
waiting_for_input = False
menu_state = "main"
level_state = ""
scene_state = ""
current_dialogue = None

known_letters = []
unknown_letters = []

#Define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colors
BLACK = (255,255,255)
WHITE = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Scenes
KITCHEN = "kitchen"
FRONT = "front"
CUSTOMER = "customer"

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

test1_img = pygame.image.load("images/test1.png").convert_alpha()
test2_img = pygame.image.load("images/test2.png").convert_alpha()


#Dialogue
SHOW_LETTER = True


#Testing dialogue
sixth_dialogue = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Now this is the letter E", font, BLACK, KITCHEN, SHOW_LETTER, "chef", "E", None)
test_word_input = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "This is how you spell tea", font, BLACK, KITCHEN, "chef", "TEA", SHOW_LETTER, sixth_dialogue)
fifth_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Very good!", font, BLACK, KITCHEN, "chef", sixth_dialogue)
fourth_dialogue = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "I am the chef, this is the letter A", font, BLACK, KITCHEN, "chef", "A", SHOW_LETTER, test_word_input)
third_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "This is the chef", font, BLACK, KITCHEN, "manager", fourth_dialogue)
second_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Blah, blah, Ill show you to the chef", font, BLACK, FRONT, "manager", third_dialogue)
first_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Hello and welcome to the restaurant", font, BLACK, FRONT,  "manager", second_dialogue)



test_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/4, "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", font, BLACK, "front",  "manager", None)

#test_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "TEST1 TEST2 TEST3 TEST4 TEST5 TEST6", font, BLACK, "front",  "manager", None)

#introduction dialogue
#AEIOU



#intro_24 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Great job, you'll get a hang of this in no time!", font, BLACK, KITCHEN,  "manager", intro_25)
#intro_24 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Great job, you'll get a hang of this in no time!", font, BLACK, KITCHEN,  "manager", intro_25)


intro_25 = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "*shows an U*", font, BLACK, KITCHEN, "chef", "U", not SHOW_LETTER, None)
intro_24 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Amazing, and last but not least lets see U", font, BLACK, KITCHEN,  "manager", intro_25)
intro_23 = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "*waits for O*", font, BLACK, KITCHEN, "chef", "O", not SHOW_LETTER, intro_24)
intro_22 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Super! let us see  O", font, BLACK, KITCHEN,  "manager", intro_23)
intro_21 = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "*waits for I*", font, BLACK, KITCHEN, "chef", "I", not SHOW_LETTER, intro_22)
intro_20 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Perfect, now I", font, BLACK, KITCHEN,  "manager", intro_21)
intro_19 = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "*waits for E*", font, BLACK, KITCHEN, "chef", "E", not SHOW_LETTER, intro_20)
intro_18 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Brilliant, lets try E", font, BLACK, KITCHEN,  "manager", intro_19)
intro_17 = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "*waits for A*", font, BLACK, KITCHEN, "chef", "A", not SHOW_LETTER, intro_18)
intro_16 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Lets start with the A", font, BLACK, KITCHEN,  "manager", intro_17)
intro_15 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Good job, now that you've done them once, lets see if you can remember them", font, BLACK, KITCHEN,  "manager", intro_16)


intro_14 = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "*shows an U*", font, BLACK, KITCHEN, "chef", "U", SHOW_LETTER, intro_15)
intro_13 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Very good, now the letter U", font, BLACK, KITCHEN,  "manager", intro_14)
intro_12 = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "*shows an O*", font, BLACK, KITCHEN, "chef", "O", SHOW_LETTER, intro_13)
intro_11 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Super! Now we do O", font, BLACK, KITCHEN,  "manager", intro_12)
intro_10 = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "*shows an I*", font, BLACK, KITCHEN, "chef", "I", SHOW_LETTER, intro_11)
intro_9 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Good job, I", font, BLACK, KITCHEN,  "manager", intro_10)
intro_8 = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "*shows an E*", font, BLACK, KITCHEN, "chef", "E", SHOW_LETTER, intro_9)
intro_7 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Very good, now the letter E", font, BLACK, KITCHEN,  "manager", intro_8)
intro_6 = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "*shows an A*", font, BLACK, KITCHEN, "chef", "A", SHOW_LETTER, intro_7)
intro_5 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2,"First, this is how you spell A, sign it back to him", font, BLACK, KITCHEN,  "manager", intro_6)

intro_4 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "This is the chef, he'll now teach you the basics", font, BLACK, KITCHEN,  "manager", intro_5)
intro_3 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Ill take you to him and teach you the basics of fingerspelling", font, BLACK, FRONT,  "manager", intro_4)
intro_2 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Our chef here only understands sign languague and fingerspelling", font, BLACK, FRONT,  "manager", intro_3)
intro_1 = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Hello and welcome to the restaurant", font, BLACK, FRONT,  "manager", intro_2)


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

#testbuttons
test1_button = button.Button(SCREEN_WIDTH/2 - test1_img.get_width()/2, SCREEN_HEIGHT-700, test1_img, 1)
test2_button = button.Button(SCREEN_WIDTH/2 + test2_img.get_width()/2, SCREEN_HEIGHT-700, test2_img, 1)

#Helper functions
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x-img.get_width()/2,y))


def checkOrderForNewLetters(dialogue):
    for word in dialogue.words:
        for letter in word.upper():
            if letter not in known_letters:
                if letter not in unknown_letters:
                    unknown_letters.append(letter)

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


DEBUG = True

#game loop
run = True

detector_initialized = False

while run:

    if detector_initialized == False:
        recognizer.initialize()
        detector_initialized = True

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
        if test1_button.draw(screen) and clicked == False:
            cust_dia = g_customer.newOrder()
            dialogue.insertDialogue(current_dialogue, current_dialogue.next, cust_dia)
            checkOrderForNewLetters(cust_dia)
            #checkDialogue()
            print(unknown_letters)
        if test2_button.draw(screen) and clicked == False:
            initial_diag = current_dialogue
            initial_next = current_dialogue.next

            '''
            1: Create dialogue for player to ask chef about new letter
            2: Create dialogue for chef to show player how to make letter
            3: player repeats letter back
            
            '''
            Latestplayer = initial_diag
            latestchef = initial_diag

            for l in unknown_letters:
                playerDiag = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "Sorry chef i don't know how to make this letter %s" %l,
                                                 font, BLACK, KITCHEN, "player", None)
                
                chefDiag = dialogue.PlayerInputDialogue(SCREEN_WIDTH/2, 
                                                        SCREEN_HEIGHT/2, 
                                                        "this is how you make the letter %s" %l,
                                                        font, 
                                                        BLACK, 
                                                        KITCHEN, 
                                                        "chef", 
                                                        l,
                                                        SHOW_LETTER,
                                                        None)
                #test_dialogue = dialogue.LinearDialogueNode(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 1, "TESTTESTTEST", font, BLACK, "front",  "manager", None)

                dialogue.insertDialogue(latestchef, initial_next, playerDiag)
                Latestplayer = playerDiag
                dialogue.insertDialogue(Latestplayer, initial_next, chefDiag)
                latestchef = chefDiag

            for l in unknown_letters:
                known_letters.append(l)
            
            unknown_letters.clear()

            print(known_letters)
            print(unknown_letters)
            print("inserted new dialogues")



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
                current_dialogue = test_dialogue
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
            current_dialogue.draw_text(screen, DEBUG)
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
                    #checkDialogue()
            else:
                user_text = event.unicode

        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and progressed_dialogue == True:
                pass
                #progressed_dialogue = False
                #print("ready to progress")
        
        if progressed_dialogue == True:
            progressed_dialogue = False
            print("ready to progress")

    pygame.display.update()


pygame.quit() 