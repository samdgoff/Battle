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
    #Replace some codes
    try:
        selected = selected.replace("~a","α")
    except:
        selected = selected.replace("~a","a")
    try:
        selected = selected.replace("~b","β")
    except:
        selected = selected.replace("~b","B")
    try:
        selected = selected.replace("~g","γ")
    except:
        selected = selected.replace("~g","y")
    try:
        selected = selected.replace("~o","Ω")
    except:
        selected = selected.replace("~o","O")
    #Return the extracted info
    return selected

def getAttribList(number, attrib, filename):
    #Get the attribute
    selected = getAttrib(number,attrib,filename)
    #Slice attribute into an array
    selected = selected.split(",")
    #Return the extracted info
    return selected

def getAttribReplaced(number, attrib, filename, replace):
    #Get the attribute
    selected = getAttrib(number,attrib,filename)
    #Replace the ~n with "replace"
    selected = selected.replace("~n",replace)
    #Return the extracted info
    return selected

def menuSetup(number, filename, addBack):
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
    if addBack == True:
        menu.append("Back")
        menuNumber += 1
        print ("  "+str(menuNumber)+") "+"Back")
    return menu

def menuSetupFromList(chosenList,enemies):
    menu = chosenList
    menuLoop = 0
    menuNumber = 0
    if enemies == True:
        for y in menu:
            if y.startswith("*"):
                menuLoop += 1
                print (getAttrib(3,int(y.replace("*","")),"config"))
            else:
                menuLoop += 1
                menuNumber += 1
                print ("  "+str(menuNumber)+") "+eName[menuLoop-1])
        for y in menu:
            if y.startswith("*"):
                menu.remove(y)
    else:
        for _ in range(2):
            menuLoop += 1
            menuNumber += 1
            print ("  "+str(menuNumber)+") "+name[menuLoop-1])
    return menu

def playerAction(who):
    global eHealth
    global health
    global eCounter
    global magic
    global counter
    global counterHealth
    global target
    damage = 0
    whoOriginal = who

    if len(eList) > 1:
        if int(getAttrib(x,5,"actions")) == 1 or int(getAttrib(x,5,"actions")) == 5: #Choose target
            whomLoop = True
            while whomLoop:
                print(getAttrib(1,22,"config"))
                playSound("towhom")
                menuSetupFromList(eList,True)
                chooseInput = input(getAttrib(1,2,"config"))
                if chooseInput.isdigit():
                    chooseInput = int(chooseInput)
                    if chooseInput < len(eList)+1 and chooseInput > 0:
                        target = chooseInput-1
                        whomLoop = False
                    else:
                        print ("   "+getAttrib(1,4,"config"))
                        playSound("error")
                else:
                    print ("   "+getAttrib(1,4,"config"))
                    playSound("error")
    else:
        target = 0

    if len(alive) > 1:
        if int(getAttrib(x,5,"actions")) == 2 or int(getAttrib(x,5,"actions")) == 3 or int(getAttrib(x,5,"actions")) == 4 or int(getAttrib(x,5,"actions")) == 6: #Choose target
            whomLoop = True
            while whomLoop:
                print(getAttrib(1,22,"config"))
                playSound("towhom")
                menuSetupFromList(alive,False)
                chooseInput = input(getAttrib(1,2,"config"))
                if chooseInput.isdigit():
                    chooseInput = int(chooseInput)
                    if chooseInput < len(alive)+1 and chooseInput > 0:
                        who = chooseInput-1
                        whomLoop = False
                    else:
                        print ("   "+getAttrib(1,4,"config"))
                        playSound("error")
                else:
                    print ("   "+getAttrib(1,4,"config"))
                    playSound("error")
    
    print (name[who]+getAttrib(x,6,"actions"))
    if int(getAttrib(x,5,"actions")) == 1: #If the action is Attack
        if cheatVar != 1:
            if random.randint(0,100) >= int(getAttrib(x,4,"actions")):
                damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
                if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                    print (getAttrib(1,8,"config"))
                if eCounter[target] == True:
                    counterCheck("player",damage,target,who)
                else:
                    print (str(damage)+" damage to "+eName[target]+"!")
                    eHealth[target] -= damage
                    playSound("attack")
            else:
                print (getAttrib(1,5,"config"))
                playSound("miss")
        else:
            damage = 999999
            print (str(damage)+" damage to "+eName[target]+"!")
            eHealth[target] -= damage
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
                if health[who] + damage >= int(getAttrib(who+1,3,"player")):
                    damage = int(getAttrib(who+1,3,"player")) - health[who]
                    print (name[who]+" is healed by "+str(damage)+" and their health is now full!")
                    health[who] += damage
                else:
                    print (name[who]+" is healed by "+str(damage)+"!")
                    health[who] += damage
                playSound("eat")

    elif int(getAttrib(x,5,"actions")) == 3: #If the action is Magic Replenish
        damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
        if damage == 0:
            print (getAttrib(1,14,"config"))
            playSound("shieldno")
        else:
            if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                print (getAttrib(1,8,"config"))
            if magic[who] + damage >= int(getAttrib(who+1,6,"player")):
                damage = int(getAttrib(who+1,6,"player")) - magic[who]
                print (name[who]+" gains "+str(damage)+" magic and it is now fully replenished!")
                magic[who] += damage
            else:
                print (name[who]+" gains "+str(damage)+" magic!")
                magic[who] += damage
            playSound("eat")

    elif int(getAttrib(x,5,"actions")) == 4: #If the action is Magic Shield
        playSound("shieldstart")
        if counter[who] == False:
            if not magic[whoOriginal] - int(getAttrib(x,3,"actions")) < 0:
                counter[who] = True
                magic[whoOriginal] -= int(getAttrib(x,3,"actions"))
                counterHealth[who] = int(getAttrib(x,2,"actions"))
                print (getAttrib(1,13,"config"))
                playSound("shieldyes")
            else:
                counter[who] = False
                print (getAttrib(1,14,"config"))
                playSound("shieldno")
        else:
            print (getAttrib(1,15,"config"))
            playSound("shieldno")

    elif int(getAttrib(x,5,"actions")) == 5: #If the action is Magic Attack
        playSound("shieldstart")
        if not magic[who] - int(getAttrib(x,8,"actions")) < 0:
            magic[who] -= int(getAttrib(x,8,"actions"))
            if random.randint(0,100) >= int(getAttrib(x,4,"actions")):
                damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
                if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                    print (getAttrib(1,8,"config"))
                if eCounter[target] == True:
                    counterCheck("player",damage,target,who)
                else:
                    print (str(damage)+" damage to "+eName[target]+"!")
                    eHealth[target] -= damage
                    playSound("attack")
            else:
                print (getAttrib(1,5,"config"))
                playSound("miss")
        else:
            counter[who] = False
            print (getAttrib(1,14,"config"))
            playSound("shieldno")

    elif int(getAttrib(x,5,"actions")) == 6: #If the action is Magic Heal
        playSound("shieldstart")
        if not magic[whoOriginal] - int(getAttrib(x,8,"actions")) < 0:
            magic[whoOriginal] -= int(getAttrib(x,8,"actions"))
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
                    if health[who] + damage >= int(getAttrib(who+1,3,"player")):
                        damage = int(getAttrib(who+1,3,"player")) - health[who]
                        print (name[who]+" is healed by "+str(damage)+" and their health is now full!")
                        health[who] += damage
                    else:
                        print (name[who]+" is healed by "+str(damage)+"!")
                        health[who] += damage
                    playSound("eat")
        else:
            counter[who] = False
            print (getAttrib(1,14,"config"))
            playSound("shieldno")

    elif int(getAttrib(x,5,"actions")) == 7: #If the action is Magic Heal (to both)
        playSound("shieldstart")
        if not magic[who] - int(getAttrib(x,8,"actions")) < 0:
            magic[who] -= int(getAttrib(x,8,"actions"))
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
                    if health[0] + damage >= int(getAttrib(1,3,"player")):
                        damage = int(getAttrib(1,3,"player")) - health[0]
                        print (name[0]+" is healed by "+str(damage)+" and their health is now full!")
                        health[0] += damage
                    else:
                        print (name[0]+" is healed by "+str(damage)+"!")
                        health[0] += damage
                    playSound("eat")
                    if health[1] + damage >= int(getAttrib(2,3,"player")):
                        damage = int(getAttrib(2,3,"player")) - health[1]
                        print (name[1]+" is healed by "+str(damage)+" and their health is now full!")
                        health[1] += damage
                    else:
                        print (name[1]+" is healed by "+str(damage)+"!")
                        health[1] += damage
                    playSound("eat")
        else:
            counter[who] = False
            print (getAttrib(1,14,"config"))
            playSound("shieldno")

    elif int(getAttrib(x,5,"actions")) == 8: #If the action is Magic Shield (to both)
        playSound("shieldstart")
        if not magic[who] - int(getAttrib(x,3,"actions")) < 0:
            magic[who] -= int(getAttrib(x,3,"actions"))
            if counter[0] == False:
                counter[0] = True
                counterHealth[0] = int(getAttrib(x,2,"actions"))
                print (getAttrib(1,13,"config"))
                playSound("shieldyes")
            else:
                print (getAttrib(1,15,"config"))
                playSound("shieldno")
            if counter[1] == False:
                counter[1] = True
                counterHealth[1] = int(getAttrib(x,2,"actions"))
                print (getAttrib(1,13,"config"))
                playSound("shieldyes")
            else:
                print (getAttrib(1,15,"config"))
                playSound("shieldno")
        else:
            print (getAttrib(1,14,"config"))
            playSound("shieldno")


def enemyAction(x,enemy):
    global eHealth
    global health
    global counter
    global nextAttack
    global eCounter
    global eCounterHealth
    damage = 0
    etarget = 0
    #Setting the enemy's target
    if health[0] <= 0:
        etarget = 1
    elif health[1] <= 0:
        etarget = 0
    else:
        if random.randint(0,100) >= 25 and health[0] != health[1]:
            if health[0] > health[1]:
                etarget = 0
            elif health[0] < health[1]:
                etarget = 1
        else:
            if random.randint(0,100) >= 50:
                etarget = 0
            else:
                etarget = 1
    nextAttack[enemy] = int(getAttrib(x,7,"actions"))
    print (eName[enemy]+getAttrib(x,6,"actions"))
    if int(getAttrib(x,5,"actions")) == 0: #If the action is Idle
        playSound("idle")
    elif int(getAttrib(x,5,"actions")) == 1: #If the action is Attack
        if cheatVar != 2:
            if random.randint(0,100) >= int(getAttrib(x,4,"actions")):
                damage = random.randint(int(getAttrib(x,2,"actions")),int(getAttrib(x,3,"actions")))
                if damage == int(getAttrib(x,3,"actions")) and int(getAttrib(x,2,"actions")) != int(getAttrib(x,3,"actions")):
                    print (getAttrib(1,12,"config"))
                if counter[etarget] == True:
                    counterCheck(enemy,damage,enemy,etarget)
                else:
                    print (str(damage)+" damage to "+name[etarget]+"!")
                    health[etarget] -= damage
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
                if eHealth[enemy] + damage >= int(getAttrib(eList[enemy],3,"enemies")):
                    damage = int(getAttrib(eList[enemy],3,"enemies")) - eHealth[enemy]
                    print (eName[enemy]+" is healed by "+str(damage)+" and their health is now full!")
                    eHealth[enemy] += damage
                else:
                    print (eName[enemy]+" is healed by "+str(damage)+"!")
                    eHealth[enemy] += damage
                playSound("eat")
        else:
            print (getAttrib(1,11,"config"))
            idle = False
            playSound("miss")

    elif int(getAttrib(x,5,"actions")) == 4: #If the action is Magic Shield
        playSound("shieldstart")
        if cheatVar != 2:
            if eCounter[enemy] == False:
                eCounter[enemy] = True
                eCounterHealth[enemy] = int(getAttrib(x,2,"actions"))
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
    status.append("null")
    if counter[0] == 1:
        status[0] = getAttrib(2,2,"config")
    else:
        status[0] = getAttrib(2,1,"config")

    status.append("null")
    if counter[1] == 1:
        status[1] = getAttrib(2,2,"config")
    else:
        status[1] = getAttrib(2,1,"config")

def eStatusSetup():
    global eStatus
    global eCounter
    global eList
    listLoop = 0
    for x in eList:
        eCounter.append(0)
        eStatus.append("null")
        if eCounter[listLoop] == 1:
            eStatus[listLoop] = getAttrib(2,2,"config")
        else:
            eStatus[listLoop] = getAttrib(2,1,"config")
        listLoop += 1

def deathCheck(who):
    global points
    global eList
    global eDead
    global eName
    global alive
    dobreak = False
    if health[0] <= 0 and 0 in alive:
        print (getAttribReplaced(1,5,"player",name[0]))
        alive.remove(0)
        playSound("die")
    if health[1] <= 0 and 1 in alive:
        print (getAttribReplaced(2,5,"player",name[1]))
        alive.remove(1)
        playSound("die")
    if not alive:
        print (getAttrib(1,9,"config"))
        battleLoop = False
        gameLoop = False
        dobreak = True
    if not who in eDead:
        if eHealth[who] <= 0:
            print (getAttribReplaced(eList[who],5,"enemies",eName[who]))
            eDead.append(who)
            playSound("die")

    for x in eDead:
        eList.pop(x)
        eName.pop(x)
        eHealth.pop(x)
        eCounter.pop(x)
        eCounterHealth.pop(x)
        try:
            eStatus.pop(x)
        except:
            pass
    eDead = []
    if not eList:
        print (getAttrib(1,3,"config"))
        battleLoop = False
        points += 1
        playSound("win")
        dobreak = True
        
    return dobreak

def counterCheck(whoStarted,damage,enemy,playerno):
    global counter
    global counterHealth
    global eCounter
    global eCounterHealth
    global health
    global eHealth
    global target
    counterLoop = True
    if whoStarted == "player":
        while counterLoop:
            if eCounter[target]:
                print ("However, "+eName[target]+"'s shield countered it!")
                eCounterHealth[target] -= damage
                playSound("shieldcounter")
                if eCounterHealth[target] <= 0:
                    eCounter[target] = False
                    print (eName[target]+"'s shield broke!")
                    playSound("shieldbreak")
            else:
                print (str(damage)+" damage to "+eName[target]+"!")
                eHealth[target] -= damage
                playSound("attack")
                counterLoop = False
                break
            
            if counter[playerno]:
                print ("However, "+name[playerno]+"'s shield countered it!")
                counterHealth[playerno] -= damage
                playSound("shieldcounter")
                if cheatVar != 4:
                    if counterHealth[playerno] <= 0:
                        counter[playerno] = False
                        print (name[playerno]+"'s shield broke!")
                        playSound("shieldbreak")
            else:
                print (str(damage)+" damage to "+name[playerno]+"!")
                health[playerno] -= damage
                playSound("attack")
                counterLoop = False
                break

    else:
        while counterLoop:
            if counter[playerno]:
                print ("However, "+name[playerno]+"'s shield countered it!")
                counterHealth[playerno] -= damage
                playSound("shieldcounter")
                if cheatVar != 4:
                    if counterHealth[playerno] <= 0:
                        counter[playerno] = False
                        print (name[playerno]+"'s shield broke!")
                        playSound("shieldbreak")
            else:
                print (str(damage)+" damage to "+name[playerno]+"!")
                health[playerno] -= damage
                playSound("attack")
                counterLoop = False
                break

            if eCounter[enemy]:
                print ("However, "+eName[enemy]+"'s shield countered it!")
                eCounterHealth[enemy] -= damage
                playSound("shieldcounter")
                if eCounterHealth[enemy] <= 0:
                    eCounter[enemy] = False
                    print (eName[enemy]+"'s shield broke!")
                    playSound("shieldbreak")
            else:
                print (str(damage)+" damage to "+eName[enemy]+"!")
                eHealth[enemy] -= damage
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
        else: count = 0
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
            else: count = 0
            textOutput.append(str(ord(x)+countArray[count]))
        temp = 'O'.join(textOutput)
        textArray = [char for char in temp]
        
        info = temp
        
        f = open("attrib/"+filename+".txt", "w")
        f.write(info)
        f.close
    except:
        pass

def enemyTurn(enemy):
    global eHealth
    global eName
    global eStatus
    global menuLoop
    global eAction
    global nextAttack
    #Enemy turn
    if not eHealth[enemy] <= 0:
        print()
        #Print whose turn it is
        print (eName[enemy]+getAttrib(1,1,"config"))
        playSound("eturn")
        print (getAttrib(1,6,"config")+str(eHealth[enemy]))
        eStatusSetup()
        print (getAttrib(1,16,"config")+eStatus[enemy])
        menu = getAttribList(eList[enemy],4,"enemies")
        if int(getAttrib(eList[enemy],6,"enemies")) == 1:
            eAction[enemy] += 1
            if eAction[enemy] == len(menu)+1: eAction[enemy] = 1
        else:
            eAction[enemy] = random.randint(1,len(menu))
        menuLoop = 0
        if nextAttack[enemy] == 0:
            for x in menu:
                menuLoop += 1
                if eAction[enemy] == menuLoop:
                    enemyAction(x,enemy)
        else:
            enemyAction(nextAttack[enemy], enemy)

def groupSetup():
    global eList

    eList = getAttribList(eGroupNumber,1,"groups")

def helpMenu(who):
    who += 1
    hLoop = True
    hdobreak = False
    print()
    while hLoop:
        print ("~HELP~")
        playSound("options")
        hMenu = menuSetup(who,"player",True)
        hInput = input("Which action do you want help with? ")
        #Make the input a usable integer
        if hInput.isdigit():
            hInput = int(hInput)
        else:
            hInput = 0
        #Check what the user has selected and do the specified action
        hMenuLoop = 0
        hUsableInput = False
        for x in hMenu:
            hMenuLoop += 1
            if hInput == hMenuLoop and x != "Back":
                hUsableInput = True
                print()
                print (getAttrib(x,1,"actions"))
                playSound("other")
                if int(getAttrib(x,5,"actions")) == 1:
                    print ("Min Damage: "+getAttrib(x,2,"actions"))
                    print ("Max Damage: "+getAttrib(x,3,"actions"))
                    print ("Miss Chance: "+getAttrib(x,4,"actions")+"%")
                elif int(getAttrib(x,5,"actions")) == 2:
                    print ("Min Health: "+getAttrib(x,2,"actions"))
                    print ("Max Health: "+getAttrib(x,3,"actions"))
                elif int(getAttrib(x,5,"actions")) == 3:
                    print ("Min Magic: "+getAttrib(x,2,"actions"))
                    print ("Max Magic: "+getAttrib(x,3,"actions"))
                elif int(getAttrib(x,5,"actions")) == 4:
                    print ("Cost: "+getAttrib(x,3,"actions"))
                    print ("Shield HP: "+getAttrib(x,2,"actions"))
                elif int(getAttrib(x,5,"actions")) == 5:
                    print ("Cost: "+getAttrib(x,8,"actions"))
                    print ("Min Damage: "+getAttrib(x,2,"actions"))
                    print ("Max Damage: "+getAttrib(x,3,"actions"))
                    print ("Miss Chance: "+getAttrib(x,4,"actions")+"%")
                elif int(getAttrib(x,5,"actions")) == 6:
                    print ("Cost: "+getAttrib(x,8,"actions"))
                    print ("Min Health: "+getAttrib(x,2,"actions"))
                    print ("Max Health: "+getAttrib(x,3,"actions"))
                elif int(getAttrib(x,5,"actions")) == 7:
                    print ("Cost: "+getAttrib(x,8,"actions"))
                    print ("Min Health: "+getAttrib(x,2,"actions"))
                    print ("Max Health: "+getAttrib(x,3,"actions"))
                elif int(getAttrib(x,5,"actions")) == 8:
                    print ("Cost: "+getAttrib(x,3,"actions"))
                    print ("Shield HP: "+getAttrib(x,2,"actions"))
                print(getAttrib(x,9,"actions"))
            elif hInput == hMenuLoop and x == "Back":
                hLoop = False
                hUsableInput = True
                hdobreak = True
        if hdobreak: break
        if hUsableInput == False:
            print (getAttrib(1,4,"config"))
            playSound("error")
            print()
        else:
            input()

#ENCRYPT STUFF

encryptFile("actions")
encryptFile("config")
encryptFile("enemies")
encryptFile("player")
encryptFile("groups")

#VARIABLES

#Enemy variables
eName = [] #str
eHealth = [] #int
eAction = [] #int
eCounter = [] #bool
eCounterHealth = [] #int
eStatus = [] #getAttrib, str
eList = []
eGroupNumber = 0
eDead = []

#Player variables
name = [] #str
health = [] #int
magic = [] #int
counter = [] #bool
counterHealth = [] #int
status = [] #getAttrib, str
target = 0
alive = []

#Global variables
damage = 0
menuLoop = 0
points = 0
nextAttack = [] #int

#Others
battleLoop = True
turnLoop = True
gameLoop = True
gameEnd = False

alphabet = [65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90]

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
quickstart = False

if cheatCode == "show me who i want to kill, these secret cheats are really brill":
    print("A cheat has been activated!")
    print("You can now choose which group of enemies you fight first!")
    playSound("cheat")
    cheatInput = input("Which group? ")
    if cheatInput.isdigit():
        eGroupNumber = int(cheatInput)-1
    else:
        eGroupNumber = 0
    quickstart = True
    print()
elif cheatCode == "the strength i need i haven't got, so make my bashing hurt a lot":
    print("A cheat has been activated!")
    print("Your attacks can't miss or be blocked and now do 999999 damage!")
    playSound("cheat")
    cheatVar = 1
    quickstart = True
    print()
elif cheatCode == "dying drives me up the wall, so now i can't be harmed at all":
    print("A cheat has been activated!")
    print("The enemy's actions cannot work anymore!")
    playSound("cheat")
    cheatVar = 2
    quickstart = True
    print()
elif cheatCode == "i never want to feel a whack, so make my shield never crack":
    print("A cheat has been activated!")
    print("Your shield cannot break!")
    playSound("cheat")
    cheatVar = 4
    quickstart = True
    print()
elif cheatCode == "this tricky game is hard to beat, so now i'll use my greatest cheat":
    print("A cheat has been activated!")
    print("Your attacks can't miss or be blocked and now do 999999 damage!")
    print("Also, you can now choose which group of enemies you fight first! Bonus!")
    playSound("cheat")
    cheatInput = input("Which group? ")
    if cheatInput.isdigit():
        eGroupNumber = int(cheatInput)-1
    else:
        eGroupNumber = 0
    cheatVar = 1
    quickstart = True
    print()
elif cheatCode == "q":
    quickstart = True
    print()

#End of cheats...

if not quickstart:
    print("To start with, what is your beautiful name? ")
    playSound("options")
    name.append("null")
    name[0] = input("Name: ")
    print()

    print("Also, what's your teddy bear's beautiful name? ")
    playSound("options")
    name.append("null")
    name[1] = input("Name: ")
    print()
else:
    name.append("Sam")
    name.append("Leopold")

health.append(0)
health[0] = int(getAttrib(1,3,"player"))
health.append(0)
health[1] = int(getAttrib(2,3,"player"))
magic.append(0)
magic.append(0)
counter.append(False)
counter.append(False)
counterHealth.append(0)
counterHealth.append(0)
alive.append(0)
alive.append(1)

while gameLoop: #Loops the whole game!
    battleLoop = True
    eGroupNumber += 1
    groupSetup()
    eDead = []
    nextAttack = []
    listLoop = 0
    toAddAlpha = {}
    for x in eList:
        eName.append("null")
        if eList.count(x) > 1:
            if not x in toAddAlpha:
                toAddAlpha[x] = -1
            toAddAlpha[x] += 1
            if toAddAlpha[x] > len(alphabet)-1: toAddAlpha[x] -= 1
            eName[listLoop] = (getAttrib(eList[listLoop],1,"enemies")+" "+chr(alphabet[toAddAlpha[x]]))
        else:
            eName[listLoop] = getAttrib(eList[listLoop],1,"enemies")
        
        eHealth.append(0)
        eHealth[listLoop] = int(getAttrib(eList[listLoop],3,"enemies"))
        eAction.append(0)
        eCounter.append(False)
        eCounterHealth.append(0)
        nextAttack.append(0)
        listLoop += 1

    print (getAttrib(4,eGroupNumber,"config"))
    playSound("other")
    input()
    
    listLoop = 0
    for x in eList:
        print (getAttribReplaced(x,2,"enemies",eName[listLoop]))
        playSound("enemy")
        listLoop+=1

    while battleLoop: #Loops the battle
        #Player turn
        turnLoop = True
        target = 0
        if not health[0] <= 0:
            while turnLoop: #Resets the player's turn if they input something that they weren't supposed to
                print()
                #Print whose turn it is
                print (name[0]+getAttrib(1,1,"config"))
                playSound("pturn")
                print (getAttrib(1,6,"config")+str(health[0]))
                print (getAttrib(1,17,"config")+str(magic[0]))
                statusSetup()
                print (getAttrib(1,16,"config")+status[0])
                #Set up the move menu
                menu = menuSetup(1,"player",False)
                #Get the user input
                actionChoice = input(getAttrib(1,2,"config"))
                actionChoiceStore = str(actionChoice)
                #Make the input a usable integer
                if actionChoice.isdigit():
                    actionChoice = int(actionChoice)
                else:
                    if actionChoiceStore.lower() == "help":
                        helpMenu(0)
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
                        playerAction(0)
                if usableInput == False and actionChoiceStore.lower() != "help":
                    print (getAttrib(1,4,"config"))
                    playSound("error")
        if deathCheck(target) == True: break

        #Teddy bear turn
        turnLoop = True
        target = 0
        if not health[1] <= 0:
            while turnLoop: #Resets the teddy bear's turn if they input something that they weren't supposed to
                print()
                #Print whose turn it is
                print (name[1]+getAttrib(1,1,"config"))
                playSound("pturn")
                print (getAttrib(1,6,"config")+str(health[1]))
                print (getAttrib(1,17,"config")+str(magic[1]))
                statusSetup()
                print (getAttrib(1,16,"config")+status[1])
                #Set up the move menu
                menu = menuSetup(2,"player",False)
                #Get the user input
                actionChoice = input(getAttrib(1,2,"config"))
                actionChoiceStore = str(actionChoice)
                #Make the input a usable integer
                if actionChoice.isdigit():
                    actionChoice = int(actionChoice)
                else:
                    if actionChoiceStore.lower() == "help":
                        helpMenu(1)
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
                        playerAction(1)
                if usableInput == False and actionChoiceStore.lower() != "help":
                    print (getAttrib(1,4,"config"))
                    playSound("error")
        if deathCheck(target) == True: break
        
        listLoop = 0
        for x in eList:
            enemyTurn(listLoop) #Enemy turn
            listLoop += 1
            dobreak = False
            if deathCheck(listLoop-1) == True:
                dobreak = True
                break
        if dobreak: break
    print()
    
    if health[0] <= 0: break

    if getAttrib(eGroupNumber+1,1,"groups") == "End":
        gameEnd = True
        break

    elif points == 1:
        print("So far, you have won 1 battle.")
    else:
        print("So far, you have won "+str(points)+" battles.")
    input("Next enemy! ")
    
    print()

if points == 0:
    print("Huh? You won no battles?")
    print("Pathetic!")
elif points == 1:
    print("You won 1 battle!")
    print("Pretty bad...")
else:
    print("You won "+str(points)+" battles!")

if gameEnd:
    print()
    print(getAttrib(1,19,"config"))
    playSound("endgame")
    if cheatVar != 0:
        input()
        print(getAttrib(1,21,"config"))
        playSound("enemy")

input()
