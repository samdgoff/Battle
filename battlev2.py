import random

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

def getAttribReplaced(number, attrib, filename):
    #Get the attribute
    selected = getAttrib(number,attrib,filename)
    #Replace the codes (e.g. ~n for name)
    selected = selected.replace("~n",getAttrib(number,1,filename))
    #Return the extracted info
    return selected

#Variables

eNumber = 2
eName = getAttrib(eNumber,1,"enemyInfo")
name = "Ness"
eHealth = 10
health = 10
damage = 0
eTurn = 0
repeat = True

#Start of program

print (getAttribReplaced(eNumber,2,"enemyInfo"))

while repeat == True:
    print (name+"'s turn!")
    print ("1) Attack")
    print ("2) Heal")
    menu = input ("  > ")
    if menu == "1":
        print("Attack")
        damage = random.randint(1,3)
        print (damage,"HP of damage to",eName+"!")
        eHealth = eHealth-damage
        if eHealth <= 0:
            print(eName,"has been slain!")
            repeat = False
            break
    elif menu == "2":
        print("Heal")
        damage = random.randint(1,5)
        print (name+" gains",damage,"HP!")
        health = health+damage
    else:
        print("Whoops! "+name+" skipped their turn!")

    print (eName+"'s turn!")
    eTurn = random.randint(1,3)
    if eTurn == 1:
        damage = random.randint(1,3)
        print (eName+" uses Bash!")
        print (damage,"HP of damage to",name+"!")
        health = health-damage
    elif eTurn == 2:
        damage = 5
        print (eName+" uses Crashing Boom Bang!")
        print (damage,"HP of damage to",name+"!")
        health = health-damage
    elif eTurn == 3:
        damage = random.randint(1,2)
        print (eName+" uses Heal")
        print (eName+" gains",damage,"HP!")
        eHealth = eHealth+damage
    if health <= 0:
            print(name,"has been slain!")
            repeat = False
            print("GAME OVER")
            break
