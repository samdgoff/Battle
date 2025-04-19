import random
import time

inputSpace = "   -> "
actionSpace = "      "
damageSpace1 = "       "
damageSpace2 = "        "
damageSpace3 = "         "
eNumber = 2
health = 100
eHealth = 100

def getAttribFromFile(eNumber, eAttrib, filename):
    f = open(filename, "rt")
    eInfo = (f.read())
    f.close()

    start = (eInfo.find("$"+str(eNumber)+"<")+3+len(str(eNumber)))
    end = (eInfo.find("$"+str(eNumber)+">")-1)
    eSection = (eInfo[start:end])

    start = (eSection.find("("+str(eAttrib)+"}")+2+len(str(eAttrib)))
    end = (eSection.find("{"+str(eAttrib)+")"))
    eSelected = (eSection[start:end])
    return eSelected

def showAttrib(eNumber, eAttrib):
    eResult = getAttribFromFile(eNumber, eAttrib, "attrib/enemyInfo.txt")
    eResult = eResult.replace("~n",getAttribFromFile(eNumber, 1, "attrib/enemyInfo.txt"))
    print (eResult)

def playSoundC1(filename,state):
    import winsound
    if state == 0:
        winsound.PlaySound(filename, winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_NOSTOP)
    elif state == 1:
        winsound.PlaySound(filename, winsound.SND_FILENAME|winsound.SND_NOSTOP)
    elif state == 2:
        winsound.PlaySound(filename, winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_LOOP|winsound.SND_NOSTOP)
    elif state == 3:
        winsound.PlaySound(filename, winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_LOOP)
    elif state == 4:
        winsound.PlaySound(filename, winsound.SND_FILENAME)
    elif state == 5:
        winsound.PlaySound(filename, winsound.SND_FILENAME|winsound.SND_ASYNC)

def printFile(filename):
    f = open(filename, "rt")
    contents = (f.read())
    print (contents)
    f.close()

def eDamage(damage,health):
    rand = random.randint(1,3)
    if (rand == 1):
        print (damageSpace1 + str(damage))
    elif (rand == 2):
        damage = damage + 1
        print (damageSpace2 + str(damage))
    elif (rand == 3):
        damage = damage + 2
        print (damageSpace3 + str(damage))
    health = health - damage
    time.sleep(0.1)
    return health

playSoundC1("music/hip_shop.wav",3)
name = input("Your name, please: ")

showAttrib(eNumber,2)
playSoundC1(getAttribFromFile(eNumber,3,"attrib/enemyInfo.txt"),3)

print (name+"'s turn:")
print ("1) "+getAttribFromFile(1,1,"attrib/menuInfo.txt"))
print ("2) "+getAttribFromFile(1,2,"attrib/menuInfo.txt"))
print ("3) "+getAttribFromFile(1,3,"attrib/menuInfo.txt"))

menuChoice = input(inputSpace).lower()

if menuChoice == "1" or menuChoice == getAttribFromFile(1,1,"attrib/menuInfo.txt").lower():
    print (actionSpace+name+" fires a clip!")
    eHealth = eDamage(10,eHealth)
    eHealth = eDamage(10,eHealth)
    eHealth = eDamage(10,eHealth)
    eHealth = eDamage(10,eHealth)
    eHealth = eDamage(10,eHealth)
    
elif menuChoice == "2" or menuChoice == getAttribFromFile(1,2,"attrib/menuInfo.txt").lower():
    print (actionSpace+name+" used an item!")
elif menuChoice == "3" or menuChoice == getAttribFromFile(1,3,"attrib/menuInfo.txt").lower():
    print (actionSpace+name+" defended!")
