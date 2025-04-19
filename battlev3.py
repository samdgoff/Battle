#IMPORTS

import random
import winsound
import tkinter as tk
from PIL import Image, ImageTk
import math

#FUNCTIONS

def getAttrib(number, attrib, filename):
    #Open and store file contents
    f = open("attrib/"+filename+".txt", "rt")
    info = (f.read())
    f.close
    #Find the section that you want
    start = (info.find("$"+str(number)+"<")+3+len(str(number)))
    end = (info.find("$"+str(number)+">")-1)
    section = (info[start:end])
    #Find the attribute that you want
    start = (section.find("("+str(attrib)+"}")+2+len(str(attrib)))
    end = (section.find("{"+str(attrib)+")"))
    selected = (section[start:end])
    #Return the extracted info
    return selected

def getAttribList(number, attrib, filename):
    #Get the attribute
    selected = getAttrib(number,attrib,filename)
    #Slice attribute into an array
    selected = selected.split(",")
    #Return the extracted info
    return selected

def getAttribReplaced(number, attrib, filename):
    #Get the attribute
    selected = getAttrib(number,attrib,filename)
    #Replace the codes (e.g. ~n for name)
    selected = selected.replace("~n",getAttrib(number,1,filename))
    #Return the extracted info
    return selected

def menuSetup(number, filename):
    menu = getAttribList(number,4,filename)
    menuLoop = 0
    menuNumber = 0
    for y in menu:
        if y.startswith("*"):
            menuLoop += 1
            print (getAttrib(3,int(y.replace("*","")),"config"))
        else:
            menuLoop += 1
            menuNumber += 1
            print ("  "+str(menuNumber)+") "+getAttrib(menu[menuLoop-1],1,"actions"))
    for y in menu:
        if y.startswith("*"):
            menu.remove(y)
    return menu

def playerAction():
    global eHealth
    global health
    global counter
    global counterHealth
    global magic
    damage = 0
    print (name+getAttrib(x,7,"actions"))
    if int(getAttrib(x,2,"actions")) == 0 and int(getAttrib(x,3,"actions")) == 0:
        if int(getAttrib(x,5,"actions")) == 0 and int(getAttrib(x,6,"actions")) == 0:
            pass
        else:
            damage = random.randint(int(getAttrib(x,5,"actions")),int(getAttrib(x,6,"actions")))
            if damage == 0:
                print (getAttrib(1,7,"config"))
                playSound("miss")
            else:
                if damage == int(getAttrib(x,6,"actions")) and int(getAttrib(x,5,"actions")) != int(getAttrib(x,6,"actions")):
                    print (getAttrib(1,8,"config"))
                if health + damage >= int(getAttrib(1,3,"player")):
                    damage = int(getAttrib(1,3,"player")) - health
                    print (name+" is healed by "+str(damage)+" and their health is now full!")
                    health += damage
                else:
                    print (name+" is healed by "+str(damage)+"!")
                    health += damage
                playSound("eat")
    else:
        if random.randint(0,100) > int(getAttrib(x,4,"actions")):
            damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
            if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                print (getAttrib(1,8,"config"))
            print (str(damage)+" damage to "+eName+"!")
            eHealth -= damage
            playSound("attack")
        else:
            print (getAttrib(1,5,"config"))
            playSound("miss")

    if int(getAttrib(x,8,"actions")) == 1:
        playSound("shieldstart")
        if counter == False:
            if not magic - int(getAttrib(x,10,"actions")) < 0:
                counter = True
                magic -= int(getAttrib(x,10,"actions"))
                counterHealth = int(getAttrib(x,9,"actions"))
                print (getAttrib(1,13,"config"))
                playSound("shieldyes")
            else:
                counter = False
                print (getAttrib(1,14,"config"))
                playSound("shieldno")
        else:
            print (getAttrib(1,15,"config"))
            playSound("shieldno")

    elif int(getAttrib(x,8,"actions")) == 2:
        damage = random.randint(int(getAttrib(x,9,"actions")),int(getAttrib(x,10,"actions")))
        if damage == 0:
            print (getAttrib(1,14,"config"))
            playSound("shieldno")
        else:
            if damage == int(getAttrib(x,10,"actions")) and int(getAttrib(x,9,"actions")) != int(getAttrib(x,10,"actions")):
                print (getAttrib(1,8,"config"))
            if magic + damage >= int(getAttrib(1,6,"player")):
                damage = int(getAttrib(1,6,"player")) - magic
                print (name+" gains "+str(damage)+" magic and it is now fully replenished!")
                magic += damage
            else:
                print (name+" gains "+str(damage)+" magic!")
                magic += damage
            playSound("eat")
        

def enemyAction():
    global eHealth
    global health
    global counter
    global counterHealth
    damage = 0
    idle = True
    print (eName+getAttrib(x,7,"actions"))
    if int(getAttrib(x,3,"actions")) == 0 and int(getAttrib(x,3,"actions")) == 0:
        if int(getAttrib(x,5,"actions")) == 0 and int(getAttrib(x,6,"actions")) == 0:
            pass
        else:
            damage = random.randint(int(getAttrib(x,5,"actions")),int(getAttrib(x,6,"actions")))
            if damage == 0:
                print (getAttrib(1,11,"config"))
                idle = False
                playSound("miss")
            else:
                if damage == int(getAttrib(x,6,"actions")) and int(getAttrib(x,5,"actions")) != int(getAttrib(x,6,"actions")):
                    print (getAttrib(1,12,"config"))
                if eHealth + damage >= int(getAttrib(eNumber,3,"enemies")):
                    damage = int(getAttrib(eNumber,3,"enemies")) - eHealth
                    print (eName+" is healed by "+str(damage)+" and their health is now full!")
                    eHealth += damage
                    idle = False
                else:
                    print (eName+" is healed by "+str(damage)+"!")
                    eHealth += damage
                    idle = False
                playSound("eat")
    else:
        if random.randint(0,100) >= int(getAttrib(x,4,"actions")):
            damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
            if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                print (getAttrib(1,12,"config"))
            if counter == True:
                print ("However, "+name+"'s shield countered it!")
                playSound("shieldcounter")
                print (str(damage)+" damage to "+eName+"!")
                eHealth -= damage
                counterHealth -= damage
                playSound("attack")
                if counterHealth <= 0:
                    counter = False
                    print (name+"'s shield broke!")
                    playSound("shieldbreak")
            else:
                print (str(damage)+" damage to "+name+"!")
                health -= damage
                playSound("attack")
            idle = False
            
        else:
            print (getAttrib(1,10,"config"))
            idle = False
            playSound("miss")
    if idle == True: playSound("idle")

def playSound(filename):
    winsound.PlaySound("audio/"+filename+".wav", winsound.SND_FILENAME)
    #pass

def statusSetup():
    global status
    global counter
    if counter == 1:
        status = getAttrib(2,2,"config")
    else:
        status = getAttrib(2,1,"config")

def deathCheck():
    global points
    dobreak = False
    if eHealth <= 0:
        print (getAttribReplaced(eNumber,5,"enemies"))
        print (getAttrib(1,3,"config"))
        battleLoop = False
        points += 1
        playSound("win")
        dobreak = True
    if health <= 0:
        print (getAttribReplaced(1,5,"player"))
        print (getAttrib(1,9,"config"))
        battleLoop = False
        gameLoop = False
        playSound("die")
        dobreak = True
    return dobreak

#VARIABLES

#Enemy variables
eNumber = 0
eName = ""
eHealth = 0
eAction = 0

#Player variables
name = getAttrib(1,1,"player")
health = 0
magic = 0
counter = False
counterHealth = 0
status = getAttrib(2,1,"config")

#Global variables
damage = 0
menuLoop = 0
points = 0

#Others
battleLoop = True
turnLoop = True
gameLoop = True
imageName = ""

#START OF PROGRAM :)

#Debug menu!
eNumber = input("Which enemy? ")
if eNumber.isdigit():
    eNumber = int(eNumber)-1
else:
    eNumber = 1
#End of debug menu

health = int(getAttrib(1,3,"player"))
magic = 0

print()

while gameLoop:
    battleLoop = True
    eNumber += 1
    eAction = 0
    
    eName = getAttrib(eNumber,1,"enemies")
    eHealth = int(getAttrib(eNumber,3,"enemies"))

    #imageName = "images/"+getAttrib(eNumber,7,"enemies")+".png"
    #window = tk.Tk()
    #img  = ImageTk.PhotoImage(Image.open(imageName))
    #lbl = tk.Label(window, image = img).pack()
    #window.mainloop()

    print (getAttribReplaced(eNumber,2,"enemies"))

    while battleLoop: #Loops the battle
        #Player turn
        turnLoop = True
        if not health <= 0:
            while turnLoop: #Resets the player's turn if they input something that they weren't supposed to
                print()
                #Print whose turn it is
                print (name+getAttrib(1,1,"config"))
                playSound("pturn")
                print (getAttrib(1,6,"config")+str(health))
                print (getAttrib(1,17,"config")+str(magic))
                statusSetup()
                print (getAttrib(1,16,"config")+status)
                #Set up the move menu
                menu = menuSetup(1,"player")
                #Get the user input
                actionChoice = input(getAttrib(1,2,"config"))
                #Make the input a usable integer
                if actionChoice.isdigit():
                    actionChoice = int(actionChoice)
                else:
                    actionChoice = 0
                #Check what the user has selected and do the specified action
                menuLoop = 0
                usableInput = False
                for x in menu:
                    menuLoop += 1
                    if actionChoice == menuLoop:
                        turnLoop = False
                        usableInput = True
                        playerAction()
                if usableInput == False:
                    print (getAttrib(1,4,"config"))
                    playSound("error")
        if deathCheck() == True: break
        #Enemy turn
        if not eHealth <= 0:
            print()
            #Print whose turn it is
            print (eName+getAttrib(1,1,"config"))
            playSound("eturn")
            print (getAttrib(1,6,"config")+str(eHealth))
            menu = getAttribList(eNumber,4,"enemies")
            if int(getAttrib(eNumber,6,"enemies")) == 1:
                eAction += 1
                if eAction == len(menu)+1: eAction = 1
            else:
                eAction = random.randint(1,len(menu))
            menuLoop = 0
            for x in menu:
                menuLoop += 1
                if eAction == menuLoop:
                    enemyAction()
        if deathCheck() == True: break
    input()
    if health <= 0: break
    print("Next enemy!")
    print()

print("You scored "+str(points)+"!")
if points == 0:
    print("What a failure!")
