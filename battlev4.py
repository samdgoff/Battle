#IMPORTS

import random
import winsound
import tkinter as tk
import math
try:
    from PIL import Image, ImageTk
except:
    pass

#FUNCTIONS

def getAttrib(number, attrib, filename):
    #Open and store file contents
    info = decryptFile(filename)
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
    global eCounter
    global magic
    global counter
    global counterHealth
    damage = 0
    print (name+getAttrib(x,6,"actions"))
    if int(getAttrib(x,5,"actions")) == 1: #If the action is Attack
        if cheatVar != 1:
            if random.randint(0,100) >= int(getAttrib(x,4,"actions")):
                damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
                if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                    print (getAttrib(1,8,"config"))
                if eCounter == True:
                    counterCheck("player",damage)
                else:
                    print (str(damage)+" damage to "+eName+"!")
                    eHealth -= damage
                    playSound("attack")
            else:
                print (getAttrib(1,5,"config"))
                playSound("miss")
        else:
            damage = 999999
            print (str(damage)+" damage to "+eName+"!")
            eHealth -= damage
            playSound("attack")

    elif int(getAttrib(x,5,"actions")) == 2: #If the action is Health Replenish
        if int(getAttrib(x,2,"actions")) == 0 and int(getAttrib(x,3,"actions")) == 0:
            pass
        else:
            damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
            if damage == 0:
                print (getAttrib(1,7,"config"))
                playSound("miss")
            else:
                if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                    print (getAttrib(1,8,"config"))
                if health + damage >= int(getAttrib(1,3,"player")):
                    damage = int(getAttrib(1,3,"player")) - health
                    print (name+" is healed by "+str(damage)+" and their health is now full!")
                    health += damage
                else:
                    print (name+" is healed by "+str(damage)+"!")
                    health += damage
                playSound("eat")

    elif int(getAttrib(x,5,"actions")) == 3: #If the action is Magic Replenish
        damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
        if damage == 0:
            print (getAttrib(1,14,"config"))
            playSound("shieldno")
        else:
            if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                print (getAttrib(1,8,"config"))
            if magic + damage >= int(getAttrib(1,6,"player")):
                damage = int(getAttrib(1,6,"player")) - magic
                print (name+" gains "+str(damage)+" magic and it is now fully replenished!")
                magic += damage
            else:
                print (name+" gains "+str(damage)+" magic!")
                magic += damage
            playSound("eat")

    elif int(getAttrib(x,5,"actions")) == 4: #If the action is Magic Shield
        playSound("shieldstart")
        if counter == False:
            if cheatVar != 3:
                if not magic - int(getAttrib(x,3,"actions")) < 0:
                    counter = True
                    magic -= int(getAttrib(x,3,"actions"))
                    counterHealth = int(getAttrib(x,2,"actions"))
                    print (getAttrib(1,13,"config"))
                    playSound("shieldyes")
                else:
                    counter = False
                    print (getAttrib(1,14,"config"))
                    playSound("shieldno")
            else:
                counter = True
                counterHealth = int(getAttrib(x,2,"actions"))
                print (getAttrib(1,13,"config"))
                playSound("shieldyes")
        else:
            print (getAttrib(1,15,"config"))
            playSound("shieldno")

def enemyAction(x):
    global eHealth
    global health
    global counter
    global nextAttack
    global eCounter
    global eCounterHealth
    damage = 0
    nextAttack = int(getAttrib(x,7,"actions"))
    print (eName+getAttrib(x,6,"actions"))
    if int(getAttrib(x,5,"actions")) == 0: #If the action is Idle
        playSound("idle")
    elif int(getAttrib(x,5,"actions")) == 1: #If the action is Attack
        if cheatVar != 2:
            if random.randint(0,100) >= int(getAttrib(x,4,"actions")):
                damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
                if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                    print (getAttrib(1,12,"config"))
                if counter == True:
                    counterCheck("enemy",damage)
                else:
                    print (str(damage)+" damage to "+name+"!")
                    health -= damage
                    playSound("attack")
            else:
                print (getAttrib(1,10,"config"))
                playSound("miss")
        else:
            print (getAttrib(1,10,"config"))
            playSound("miss")
    
    elif int(getAttrib(x,5,"actions")) == 2: #If the action is Health Replenish
        if cheatVar != 2:
            damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
            if damage == 0:
                print (getAttrib(1,11,"config"))
                idle = False
                playSound("miss")
            else:
                if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                    print (getAttrib(1,12,"config"))
                if eHealth + damage >= int(getAttrib(eNumber,3,"enemies")):
                    damage = int(getAttrib(eNumber,3,"enemies")) - eHealth
                    print (eName+" is healed by "+str(damage)+" and their health is now full!")
                    eHealth += damage
                else:
                    print (eName+" is healed by "+str(damage)+"!")
                    eHealth += damage
                playSound("eat")
        else:
            print (getAttrib(1,11,"config"))
            idle = False
            playSound("miss")

    elif int(getAttrib(x,5,"actions")) == 4: #If the action is Magic Shield
        playSound("shieldstart")
        if cheatVar != 2:
            if eCounter == False:
                eCounter = True
                eCounterHealth = int(getAttrib(x,2,"actions"))
                print (getAttrib(1,18,"config"))
                playSound("shieldyes")
            else:
                print (getAttrib(1,15,"config"))
                playSound("shieldno")
        else:
            print (getAttrib(1,15,"config"))
            playSound("shieldno")

def playSound(filename):
    try:
        winsound.PlaySound("audio/"+filename+".wav", winsound.SND_FILENAME)
    except:
        pass

def statusSetup():
    global status
    global counter
    if counter == 1:
        status = getAttrib(2,2,"config")
    else:
        status = getAttrib(2,1,"config")

def eStatusSetup():
    global eStatus
    global eCounter
    if eCounter == 1:
        eStatus = getAttrib(2,2,"config")
    else:
        eStatus = getAttrib(2,1,"config")

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

def counterCheck(whoStarted,damage):
    global counter
    global counterHealth
    global eCounter
    global eCounterHealth
    global health
    global eHealth
    counterLoop = True
    if whoStarted == "player":
        while counterLoop:
            if eCounter:
                print ("However, "+eName+"'s shield countered it!")
                eCounterHealth -= damage
                playSound("shieldcounter")
                if eCounterHealth <= 0:
                    eCounter = False
                    print (eName+"'s shield broke!")
                    playSound("shieldbreak")
            else:
                print (str(damage)+" damage to "+eName+"!")
                eHealth -= damage
                playSound("attack")
                counterLoop = False
                break
            
            if counter:
                print ("However, "+name+"'s shield countered it!")
                counterHealth -= damage
                playSound("shieldcounter")
                if cheatVar != 4:
                    if counterHealth <= 0:
                        counter = False
                        print (name+"'s shield broke!")
                        playSound("shieldbreak")
            else:
                print (str(damage)+" damage to "+name+"!")
                health -= damage
                playSound("attack")
                counterLoop = False
                break

    if whoStarted == "enemy":
        while counterLoop:
            if counter:
                print ("However, "+name+"'s shield countered it!")
                counterHealth -= damage
                playSound("shieldcounter")
                if cheatVar != 4:
                    if counterHealth <= 0:
                        counter = False
                        print (name+"'s shield broke!")
                        playSound("shieldbreak")
            else:
                print (str(damage)+" damage to "+name+"!")
                health -= damage
                playSound("attack")
                counterLoop = False
                break

            if eCounter:
                print ("However, "+eName+"'s shield countered it!")
                eCounterHealth -= damage
                playSound("shieldcounter")
                if eCounterHealth <= 0:
                    eCounter = False
                    print (eName+"'s shield broke!")
                    playSound("shieldbreak")
            else:
                print (str(damage)+" damage to "+eName+"!")
                eHealth -= damage
                playSound("attack")
                counterLoop = False
                break

def decryptFile(filename):
    f = open("attrib/"+filename+".txt", "rt")
    info = (f.read())
    f.close
    textArray = info.split("O")
    textOutput = []
    
    count = 0
    countArray = [182346,234,345098,12309857,23059687,3245,20679823175,234,24645365067234,12434534]
    for x in textArray:
        if count != (len(countArray)-2): count += 1
        else: counter = 0
        textOutput.append(chr(int(x)-countArray[count]))
    temp = ''.join(textOutput)
    textArray = [char for char in temp]
    
    info = temp
    
    return info

def encryptFile(filename):
    try:
        f = open("attrib/decrypted/"+filename+".txt", "rt")
        info = (f.read())
        f.close
        textArray = [char for char in info]
        textOutput = []
        
        count = 0
        countArray = [182346,234,345098,12309857,23059687,3245,20679823175,234,24645365067234,12434534]
        for x in textArray:
            if count != (len(countArray)-2): count += 1
            else: counter = 0
            textOutput.append(str(ord(x)+countArray[count]))
        temp = 'O'.join(textOutput)
        textArray = [char for char in temp]
        
        info = temp
        
        f = open("attrib/"+filename+".txt", "w")
        f.write(info)
        f.close
    except:
        pass

#ENCRYPT STUFF

encryptFile("actions")
encryptFile("config")
encryptFile("enemies")
encryptFile("player")

#VARIABLES

#Enemy variables
eNumber = 0
eName = ""
eHealth = 0
eAction = 0
eCounter = False
eCounterHealth = 0
eStatus = getAttrib(2,1,"config")

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
nextAttack = 0

#Others
battleLoop = True
turnLoop = True
gameLoop = True
gameEnd = False
imageName = ""

#START OF PROGRAM :)

print("""
  ____                  _          _                        _             
 / ___|  __ _ _ __ ___ ( )___     / \   _ __ ___   __ _ ___(_)_ __   __ _ 
 \___ \ / _` | '_ ` _ \|// __|   / _ \ | '_ ` _ \ / _` |_  / | '_ \ / _` |
  ___) | (_| | | | | | | \__ \  / ___ \| | | | | | (_| |/ /| | | | | (_| |
 |____/ \__,_|_| |_| |_| |___/ /_/   \_\_| |_| |_|\__,_/___|_|_| |_|\__, |
         ____        _   _   _         ____                      _  |___/ 
        | __ )  __ _| |_| |_| | ___   / ___| __ _ _ __ ___   ___| |       
        |  _ \ / _` | __| __| |/ _ \ | |  _ / _` | '_ ` _ \ / _ \ |       
        | |_) | (_| | |_| |_| |  __/ | |_| | (_| | | | | | |  __/_|       
        |____/ \__,_|\__|\__|_|\___|  \____|\__,_|_| |_| |_|\___(_)       

""")
print(getAttrib(1,20,"config"))
cheatCode = input()

#Cheats! Oh yeah!

cheatVar = 0

if cheatCode == "show me who i want to kill, these secret cheats are really brill":
    print("A cheat has been activated!")
    print("You can now choose which enemy you fight first!")
    playSound("cheat")
    eNumber = input("Which enemy? ")
    if eNumber.isdigit():
        eNumber = int(eNumber)-1
    else:
        eNumber = 1
    print()
elif cheatCode == "the strength i need i haven't got, so make my bashing hurt a lot":
    print("A cheat has been activated!")
    print("Your attacks can't miss or be blocked and now do 999999 damage!")
    playSound("cheat")
    cheatVar = 1
    print()
elif cheatCode == "dying drives me up the wall, so now i can't be harmed at all":
    print("A cheat has been activated!")
    print("The enemy's actions cannot work anymore!")
    playSound("cheat")
    cheatVar = 2
    print()
elif cheatCode == "refilling magic's such a chore, so it won't go away no more":
    print("A cheat has been activated!")
    print("You no longer use up any magic!")
    playSound("cheat")
    cheatVar = 3
    print()
elif cheatCode == "i never want to feel a whack, so make my shield never crack":
    print("A cheat has been activated!")
    print("Your shield cannot break!")
    playSound("cheat")
    cheatVar = 4
    print()
elif cheatCode == "this tricky game is hard to beat, so now i'll use my greatest cheat":
    print("A cheat has been activated!")
    print("Your attacks can't miss or be blocked and now do 999999 damage!")
    print("Also, you can now choose which enemy you fight first! Bonus!")
    playSound("cheat")
    eNumber = input("Which enemy? ")
    if eNumber.isdigit():
        eNumber = int(eNumber)-1
    else:
        eNumber = 1
    cheatVar = 1
    print()

#End of cheats...

health = int(getAttrib(1,3,"player"))
magic = 0

while gameLoop:
    battleLoop = True
    eAction = 0
    nextAttack = 0
    
    eNumber += 1
    
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
            eStatusSetup()
            print (getAttrib(1,16,"config")+eStatus)
            menu = getAttribList(eNumber,4,"enemies")
            if int(getAttrib(eNumber,6,"enemies")) == 1:
                eAction += 1
                if eAction == len(menu)+1: eAction = 1
            else:
                eAction = random.randint(1,len(menu))
            menuLoop = 0
            if nextAttack == 0:
                for x in menu:
                    menuLoop += 1
                    if eAction == menuLoop:
                        enemyAction(x)
            else:
                enemyAction(nextAttack)
        if deathCheck() == True: break

    print()
    
    if health <= 0: break

    if getAttrib(eNumber+1,1,"enemies") == "End":
        gameEnd = True
        break

    elif points == 1:
        print("So far, you have killed 1 enemy.")
    else:
        print("So far, you have killed "+str(points)+" enemies.")
    input("Next enemy! ")
    
    print()

if points == 0:
    print("Huh? You killed nothing? Not even "+getAttrib(1,1,"enemies")+"?")
    print("Pathetic!")
elif points == 1:
    print("You killed 1 enemy!")
    print("Pretty bad...")
else:
    print("You killed "+str(points)+" enemies!")

if gameEnd:
    print()
    print(getAttrib(1,19,"config"))
    playSound("endgame")
    if cheatVar != 0:
        input()
        print(getAttrib(1,21,"config"))

input()
