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
        self.location = 'start'

myPlayer = player()

#Title screen

def title_screen_selections():
    option = input("> ")
    if option.lower() == "play":
        start_game()  #placeholder
    elif option.lower() == "help":
        help_menu()
    elif option.lower() == "quit":
        sys.exit()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Please enter a valid command.")
        option = input("> ")
        if option.lower()=="play":
            start_game()  #placeholder
        elif option.lower() == "help":
            help_menu()     #placeholder
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
    print("   -Use arrows to move-   ")
    print("   -Type the commands-   ")
    print("   -Use 'look' to inspect something-   ")
    title_screen_selections()
title_screen()


#Map, start at b2
--------------
| |  | |  | |    a1...
--------------
| |  |S|  | |    b1...
--------------
| |  | |  |E|    c1...
--------------

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
        'a1'={
        ZONENAME = ''
        DESCRIPTION = "Description"
        EXAMINATION = "Examine"
        SOLVED = False
        UP = ''
        DOWN = 'b1'
        LEFT = ''
        RIGHT = 'a2'},

        'a2'={
        ZONENAME = ''
        DESCRIPTION = "Description"
        EXAMINATION = "Examine"
        SOLVED = False
        UP = ''
        DOWN = 'b2'
        LEFT = 'a1'
        RIGHT = 'a3'},

        'a3'={
        ZONENAME = ''
        DESCRIPTION = "Description"
        EXAMINATION = "Examine"
        SOLVED = False
        UP = ''
        DOWN = 'b3'
        LEFT = 'a2'
        RIGHT = ''},

        'b2'={
        ZONENAME = 'Living room'
        DESCRIPTION = "A cozy, big room with a sofa and a chimney"
        EXAMINATION = "The fire is burning and you can see four doors in its light."
        SOLVED = False
        UP = 'a2'
        DOWN = 'c2'
        LEFT = 'b1'
        RIGHT = 'b3'},

        'b1'={
        ZONENAME = 'Kitchen'
        DESCRIPTION = "Description"
        EXAMINATION = "Examine"
        SOLVED = False
        UP = 'a1'
        DOWN = 'c1'
        LEFT = ''
        RIGHT = 'b2'},

        'b3'={
        ZONENAME = 'Workshop'
        DESCRIPTION = "Description"
        EXAMINATION = "Examine"
        SOLVED = False
        UP = 'a3'
        DOWN = 'c3'
        LEFT = 'b2'
        RIGHT = ''},

        'c1'={
        ZONENAME = ''
        DESCRIPTION = "Description"
        EXAMINATION = "Examine"
        SOLVED = False
        UP = 'b1'
        DOWN = ''
        LEFT = ''
        RIGHT = 'c2'},

        'c2'={
        ZONENAME = ''
        DESCRIPTION = "Description"
        EXAMINATION = "Examine"
        SOLVED = False
        UP = 'b2'
        DOWN = ''
        LEFT = 'c1'
        RIGHT = 'c3'},

        'c3'={
        ZONENAME = ''
        DESCRIPTION = "Description"
        EXAMINATION = "Examine"
        SOLVED = False
        UP = 'b3'
        DOWN = ''
        LEFT = 'c2'
        RIGHT = ''},
}



#Game Interactivity
def print_location():
    print('\n' + ('#' * (4 + len(myPlayer.location))))



#Game Functionality

def start_game():
