print("You wake up in a room. Just a blank, white room with nothing in it. There is a door in front of you. ")
print("Available commands: 'use door'")
MLdescription=open("MLdescription.txt")
note=open("note.txt")
Kitchendescription=open("Kitchendescription.txt")
Officesdescription=open("Officesdescription.txt")
Exitdescription=open("Exitdescription.txt")
Endgame=open("Endgame.txt")


def whereAt(pos):
    if pos=="main lobby":
        for l in MLdescription:
            print (l)
    elif pos=="kitchen":
        for l in Kitchendescription:
            print(l)
    elif pos=="offices":
        for l in Officesdescription:
            print(l)
    elif pos=="exit":
        for l in Exitdescription:
            print (l)
    elif pos=="end":
        for l in Endgame:
            print(l)                     #Function that loads a txt description of a room

kitcheninv=['knife', '1sthalf']
def Kitchen():
    action=""
    pos="kitchen"
    leave=""
    whereAt(pos)
    while leave!="y":
        if 'knife' not in playerinv and '1sthalf' not in playerinv:
            action=input("Available actions: 'take knife', 'take paper'   ")
        elif 'knife' in playerinv and "1sthalf" not in playerinv:
            action=input("Available actions: 'take paper'   ")
        elif '1sthalf' in playerinv and "knife" not in playerinv:
            action=input("Available actions: take knife   ")
        elif '1sthalf' and 'knife' in playerinv:
            action=""
            print("Nothing interesting left here")
            print("")

        if action=="take knife":
            kitcheninv.remove("knife")
            playerinv.append("knife")
            print("You have picked up a knife. ")
        elif action=="take paper":
            kitcheninv.remove("1sthalf")
            playerinv.append("1sthalf")
            print("You unfold the paper. It says '040'")


        print("Do you want to visit another room?  (y/n)   ")
        leave=input("")

    return playerinv                        #Function responsible for kitchen

officesinv=["2ndhalf", "stuckcard"]
def Offices():
    action=""
    knifecut=""
    pos="offices"
    leave=""
    whereAt(pos)
    while leave!="y":
        knifecut=""
        if "2ndhalf" not in playerinv and "keycard" not in playerinv:
            action=input("Available actions: take paper, look card    ")
        elif "2ndhalf" not in playerinv and "keycard" in playerinv:
            action=input("Available actions: take paper   ")
        elif "2ndhalf" in playerinv and "keycard" not in playerinv:
            action=("Available actions: look card    ")
        elif "2ndhalf" in playerinv and "keycard" in playerinv:
            action=""
            print("Nothing interesting left here.")

        if action=="take paper":
            officesinv.remove("2ndhalf")
            playerinv.append("2ndhalf")
            print("You have picked up a piece of paper. It is torn on the left side. It says '319'   ")
        elif action=="look card":
            print("The card is stuck to the table. Perhaps something sharp would help.")

        if "knife" in playerinv and "stuckcard" in officesinv:
            knifecut=input("You have a knife in your hand. Do you want to use it on a card? (y/n)  ")

        if knifecut=="y":
            officesinv.remove("stuckcard")
            officesinv.append("freecard")
            playerinv.append("keycard")
            print("You have used the knife to cut the glue and collect the card.")
        elif knifecut=="n":
            pass

        print("Do you want to visit another room?  (y/n)   ")
        leave=input("")

    return playerinv                         #Function responsible for offices

def Exit():
    action=""
    userinv=""
    codeentered=0
    keycheck=0
    exit=0
    leave=""
    pos = "exit"
    whereAt(pos)

    while exit!=1 or leave!="y":
        print("This place is quiet enough. You can concentrate and manage items in your inventory. ")
        action=input("Available actions: check inventory, enter code, use keycard.      ")
        if action=="check inventory":
            print("Items in your inventory: ")
            for f in playerinv:
                print(f)
        elif action=="enter code":
            if input("You approach the console. What is your guess?        ")!="040319":
                print("ACCESS DENIED")
            else:
                print("ACCESS GRANTED")
                codeentered=1
        elif action=="use keycard":
            if "keycard" in playerinv:
                print("You swipe the keycard. The panel makes a loud beep.   ")
                keycheck=1
            elif "keycard" not in playerinv:
                print("You dont have a keycard.")

        if keycheck + codeentered ==2:
            exit=1
            return exit
        if exit!=1:
            leave=input("Do you want to leave the room and try again later? (y/n)    ")                             #Exit and endgame function


playerinv=[]
check=input("")                           #starts the game
pos=""
if check=="use door":
    pos="main lobby"
else:
    print("Unknown command")
if pos=="main lobby":
    whereAt(pos)
print("Actions available: 'go kitchen', 'go offices', 'read note'")
resp=input("What are your actions?          ")
if resp=='read note':
    print("You pick up the note and read it. It says:")
    print("")
    for l in note:
        print(l)
else:
    if resp=='go kitchen':
        playerinv=Kitchen()
    elif resp == "go offices":
        playerinv=Offices()

while exit!=1:                               #the loop allows to navigate between the rooms and updates the inventory
    print("Where do you go next?")
    print("")
    place=input("Available options: offices, kitchen, exit.     ")
    if place=="offices":
        playerinv.append(Offices())
    elif place=="kitchen":
        playerinv.append(Kitchen())
    elif place=="exit":
        exit=Exit()
pos="end"                                    #ends the game
whereAt(pos)
