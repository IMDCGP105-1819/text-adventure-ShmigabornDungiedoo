import sys
import cmd
import os
import textwrap
import time
import random

screen_width = 100

#Player setup

class player:
    def __init__(self):
        self.name = ''
        self.inventory=[]
        self.location = 'b2'
        self.gameOver= False

myPlayer = player()

#Title screen

def title_screen_selections():
    option = input("> ")
    if option.lower() == "play":
        game_setup()
    elif option.lower() == "help":
        help_menu()
    elif option.lower() == "quit":
        sys.exit()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Please enter a valid command.")
        option = input("> ")
        if option.lower()=="play":
            game_setup()
        elif option.lower() == "help":
            help_menu()
        elif option.lower() == "quit":
            sys.exit()


def title_screen():
    os.system ('cls')
    print("////////////////////")
    print("Welcome to the Game!")
    print("")
    print("   -play-   ")
    print("   -help-   ")
    print("   -quit-   ")
    title_screen_selections()

def help_menu():
    print("   -You can move up, down, left and right-   ")
    print("   -Type the commands-   ")
    print("   -Use 'examine' to inspect something-   ")
    print("   -Use 'inventory' to check your inventory-    ")
    title_screen_selections()


#Map, start at b2
#--------------
#| |  |R|  | |    a1...
#--------------
#|R|  |S|  |R|    b1...
#--------------
#| |  |R|  |E|    c1...
#--------------

ZONENAME = ''
DESCRIPTION = "Description"
EXAMINATION = "Examine"
SOLVED = False
UP = "up", "north"
DOWN = "down", "south"
LEFT = "left", "west"
RIGHT = "right", "east"

solved_places = {'a1':False, 'a2':False, 'a3':False,
                 'b1':False, 'b2':False, 'b3':False,
                 'c1':False, 'c2':False, 'c3':False,
                 }

zonemap={
        'a1': {
        ZONENAME: 'Corridor',
        DESCRIPTION: "Just a normal corridor",
        EXAMINATION: "The floors are wooden and the walls are painted in grey",
        SOLVED: False,
        UP: '',
        DOWN: 'b1',
        LEFT: '',
        RIGHT: 'a2'},

        'a2':{
        ZONENAME: 'Master Bedroom',
        DESCRIPTION: "A spacious bedroom with a huge bed, a closet and a weird device on the wall. When you walk in, the door closes.",
        EXAMINATION: "The device is a card reader. Perhaps you could find a card somewhere in the room.",
        SOLVED: False,
        UP: '',
        DOWN:'b2',
        LEFT: 'a1',
        RIGHT: 'a3'},

        'a3':{
        ZONENAME: 'Corridor',
        DESCRIPTION: "Just a normal corridor",
        EXAMINATION:"The floors are wooden and the walls are painted in grey",
        SOLVED: False,
        UP: '',
        DOWN: 'b3',
        LEFT: 'a2',
        RIGHT: ''},

        'b2':{
        ZONENAME: 'Living room',
        DESCRIPTION: "A cozy, big room with a sofa and a chimney",
        EXAMINATION: "The fire is burning and you can see four doors in its light.",
        SOLVED: False,
        UP: 'a2',
        DOWN: 'c2',
        LEFT: 'b1',
        RIGHT: 'b3'},

        'b1':{
        ZONENAME: 'Kitchen',
        DESCRIPTION: "An old, dusty kitchen. You can see something stuck to the wall. When you walk in, the door closes.",
        EXAMINATION: "You look closer. It is a small red key. It is firmly stuck. Perhaps a knife would help.",
        SOLVED: False,
        UP: 'a1',
        DOWN: 'c1',
        LEFT: '',
        RIGHT: 'b2'},

        'b3':{
        ZONENAME: 'Workshop',
        DESCRIPTION: "Description",
        EXAMINATION: "Examine",
        SOLVED: False,
        UP: 'a3',
        DOWN: 'c3',
        LEFT: 'b2',
        RIGHT: ''},

        'c1':{
        ZONENAME: 'Corridor',
        DESCRIPTION: "Just a normal corridor",
        EXAMINATION:"The floors are wooden and the walls are painted in grey",
        SOLVED: False,
        UP: 'b1',
        DOWN: '',
        LEFT: '',
        RIGHT: 'c2'},

        'c2':{
        ZONENAME: '',
        DESCRIPTION: "Description",
        EXAMINATION: "Examine",
        SOLVED: False,
        UP: 'b2',
        DOWN: '',
        LEFT: 'c1',
        RIGHT: 'c3'},

        'c3':{
        ZONENAME: '',
        DESCRIPTION: "Description",
        EXAMINATION: "Examine",
        SOLVED: False,
        UP: 'b3',
        DOWN: '',
        LEFT: 'c2',
        RIGHT: ''},
}



#Game Interactivity
def print_location():
    print('\n' + ('#' * (4 + len(myPlayer.location))))
    print('# '+ zonemap[myPlayer.location][ZONENAME] + ' #')
    print('# ' + zonemap[myPlayer.location] [DESCRIPTION] + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.location))))

def prompt():
    print("\n")
    print("What would you like to do?")
    action=input("> ")
    acceptable_actions=('move', 'walk', 'go', 'travel', 'quit', 'examine', 'inspect', 'interact', 'look')
    while action.lower() not in acceptable_actions:
        print("Unknown action, try again.\n")
        action = input("> ")
    if action.lower()=='quit':
        sys.exit()
    elif action.lower() in ['move', 'walk', 'go', 'travel']:
        player_move (action.lower())
    elif action.lower() in ['examine', 'inspect', 'interact', 'look']:
        player_examine(action.lower())
    elif action.lower() =='inventory':
        print(myPlayer.inventory)

def player_move(myAction):
    print("Where do you want to go?")
    dest = input("> ")
    if dest in ["up", "north"]:
        destination = zonemap [myPlayer.location][UP]
        movement_func(destination)
    elif dest in ['down', 'south']:
        destination = zonemap [myPlayer.location][DOWN]
        movement_func(destination)
    elif dest in ['left', 'west']:
        destination = zonemap [myPlayer.location][LEFT]
        movement_func(destination)
    elif dest in ['right', 'east']:
        destination = zonemap [myPlayer.location][RIGHT]
        movement_func(destination)


def player_examine(action):
    print(zonemap[myPlayer.location][EXAMINATION])
    if zonemap[myPlayer.location][ZONENAME]== 'Master Bedroom' :
        while zonemap[myPlayer.location][SOLVED]!= True:
            print("What do you check?\n")
            q=input("> ")
            if q == 'closet':
                print("Just some old clothes.\n")
            elif q== 'bed':
                print("You have found a small green key, which you keep, and a keycard.\n")
                print("You use the keycard on the device and the door opens.\n")
                myPlayer.inventory.append("greenKey")
                zonemap[myPlayer.location][SOLVED]=True
    elif zonemap[myPlayer.location][ZONENAME] =='Kitchen':
        while zonemap[myPlayer.location][SOLVED]!= True:
            print("There are a few knives nearby. What do you do?\n")
            q=input("> ")
            if q in ["take knife", "use knife"]:
                print("You take the knife and tear the key off the wall. The door opens.\n")
                myPlayer.inventory.append("redKey")
                zonemap[myPlayer.location][SOLVED]=True
            else:
                print("Invalid input.")
    #elif zonemap[myPlayer.location] ==b3:
        #print()
    #elif zonemap[myPlayer.location] ==c2:
        #print()



def movement_func(destination):
    print("\n" + "You have moved to the " + destination + ".")
    myPlayer.location = destination
    print_location()

#Game Functionality


def game_loop():
    while myPlayer.gameOver == False:
        prompt()

def game_setup():
    os.system("cls")
    q1="What is your name?\n"
    for c in q1:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)
    p_name=input("> ")
    myPlayer.name=p_name

    s1="Welcome. Your goal is to solve all puzzles and find 4 keys.\n"
    s2="Until then you are stuck in this house.\n"
    s3="Only four out of nine rooms have puzzles. Each room can be solved without items from other rooms\n"
    s4="Good luck.\n"
    for c in s1:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.03)
    for c in s2:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.03)
    for c in s3:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.03)
    for c in s4:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.03)
    game_loop()

title_screen()
