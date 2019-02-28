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
UP = "up", "north"  #Directions a player can move in
DOWN = "down", "south"
LEFT = "left", "west"
RIGHT = "right", "east"
#checks if the room is solved.
solved_places = {'a1':False, 'a2':False, 'a3':False,
                 'b1':False, 'b2':False, 'b3':False,
                 'c1':False, 'c2':False, 'c3':False,
                 }
#Stores most of the room information
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
        DESCRIPTION: "A spacious bedroom with a huge bed, a closet and a weird device on the wall.",
        EXAMINATION: "When you enter deeper in the room, the door locks behind you. The device is a card reader. Perhaps you could find a card somewhere in the room.",
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
        DESCRIPTION: "An old, dusty kitchen. You can see something stuck to the wall.",
        EXAMINATION: "When you enter deeper in the room, the door locks behind you. You look closer. It is a small red key. It is firmly stuck. Perhaps a knife would help.",
        SOLVED: False,
        UP: 'a1',
        DOWN: 'c1',
        LEFT: '',
        RIGHT: 'b2'},

        'b3':{
        ZONENAME: 'Workshop',
        DESCRIPTION: "A rather spacious workshop. An old wooden working table is standing next to the wall. A lot of cabinets fill most of the room. All of them are marked with animal pictures.",
        EXAMINATION: "When you enter deeper in the room, the door locks behind you. You search the working table and find a diary. After reading it, you find out that the owner was fond of egyptian mythology and, especially of Ra. This gives you an idea. Which animal is Ra portrayed as? ",
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
        ZONENAME: 'Museum',
        DESCRIPTION: "This room looks like a museum dedicated to World War II. In the middle is a huge painting with a date at the bottom.",
        EXAMINATION: "When you enter deeper in the room, the door locks behind you. You look closer at the date under the painting. It says ' 1900 - 1900'. The las two digits of both years can spin. Perhaps correcting the date would help? You decide to rotate the numbers.",
        SOLVED: False,
        UP: 'b2',
        DOWN: '',
        LEFT: 'c1',
        RIGHT: 'c3'},

        'c3':{
        ZONENAME: 'Exit',
        DESCRIPTION: "This is a dead end. Only 1 door is in the room.",
        EXAMINATION: "When you look closer - you seee 4 key holes of different colours.",
        SOLVED: False,
        UP: 'b3',
        DOWN: '',
        LEFT: 'c2',
        RIGHT: ''},
}



#Game Interactivity


#Prints out the location and its DESCRIPTION
def print_location():
    print('\n' + ('#' * (4 + len(myPlayer.location))))
    print('# '+ zonemap[myPlayer.location][ZONENAME] + ' #')
    print('# ' + zonemap[myPlayer.location] [DESCRIPTION] + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.location))))

#Actions that are available at any time.
def prompt():
    print("\n")
    print("What would you like to do?")
    action=input("> ")
    acceptable_actions=('move', 'walk', 'go', 'travel', 'quit', 'examine', 'inspect', 'interact', 'look', 'inventory')
    while action.lower() not in acceptable_actions:  #checks if the input is acceptable, if not - says so and asks again.
        print("Unknown action, try again.\n")
        action = input("> ")
    if action.lower()=='quit': # allows to quit the game.
        sys.exit()
    elif action.lower() in ['move', 'walk', 'go', 'travel']: # allows to move between adjacent roooms
        player_move (action.lower())
    elif action.lower() in ['examine', 'inspect', 'interact', 'look']: # gives more info about the room. essential to sloving riddles.
        player_examine(action.lower())
    elif action.lower() =='inventory': # allows to check the inventory
        print(myPlayer.inventory)

def player_move(myAction): # This function calls the destination from a dictionary above, and puts that value into the function which displays the movement.
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


def player_examine(action): #stores all the riddles for the rooms. Activated after examining the room.
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
    elif zonemap[myPlayer.location][ZONENAME] =='Workshop':
        while zonemap[myPlayer.location][SOLVED]!= True:
            q= input("> ")
            if q.lower() == "falcon":
                print("You open the cabinet with a falcon on it. Inside is a small yellow key. As soon as you take it, the door behind you opens.")
                zonemap[myPlayer.location][SOLVED]=True
                myPlayer.inventory.append("yellowKey")
            else:
                print("You check the cabinet with that creature. It is empty. Think again.")

    elif zonemap[myPlayer.location][ZONENAME] =="Museum":
        while zonemap[myPlayer.location][SOLVED]!= True:
            print("What 2 number do you put in the first year?")
            q=int(input("> "))
            print("And the second?")
            p=int(input("> "))
            if q== 39 and p == 45:
                print("When you enter those numbers, the painting moves apart and reveals a small blue key. When you take it, the door behind you opens.")
                myPlayer.inventory.append("blueKey")
                zonemap[myPlayer.location][SOLVED]=True
            else:
                print("Nothing happens. Perhaps the date is wrong?")
    elif zonemap[myPlayer.location][ZONENAME] =="Exit":
        q = ["redKey", "blueKey", "greenKey", "yellowKey"]
        if "redKey" in myPlayer.inventory and "blueKey" in myPlayer.inventory and "yellowKey" in myPlayer.inventory and "greenKey" in myPlayer.inventory:
            print("You have all the keys. Would you like to leave this house?")
            i = input("> ")
            if i == "yes":
                myPlayer.gameOver = True
            else:
                 print("You decide to stay in the house for a bit longer.")
        else:
            print("You dont have all the keys yet. Go explore some more.")





def movement_func(destination): #confirms that the player has moved to a different room
    print("\n" + "You have moved to the " + destination + ".")
    myPlayer.location = destination
    print_location()

#Game Functionality

def endgame():# outputs the ending sequence
    end1=("You put the keys in one after another. When you turn the last key the door clicks and opens. The sun is shining and a blow of fresh air washes over you. You are free.")
    for c in end1:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)
        input("Press any key to quit.")

def game_loop():#loops the game
    while myPlayer.gameOver == False:
        prompt()
    endgame()

def game_setup():#clears the command line and starts the game
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
        sys.stdout.write(c)    #these are used to make the text appear letter by letter
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
#sarts the game
title_screen()
