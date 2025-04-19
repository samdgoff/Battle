import random

eName = "Groblin"
name = "Player"
eHealth = 10
health = 10
damage = 0
eTrun = 0
repeat = True

print (name+" encountered a "+eName+"!")

while repeat == True:
    print (name+"'s turn!")
    print ("1) Attack")
    print ("2) Heal")
    menu = input ("  > ")
    if menu == "1":
        print("YES YES ATTACK BOI")
        
        input("Press enter to attack!")
        damage = random.randint(1,3)
        print (damage,"HP of damage to",eName+"!")
        eHealth = eHealth-damage
        if eHealth <= 0:
            print(eName,"has been slain!")
            repeat = False
    elif menu == "2":
        print("YES YES HEAL BOI")
        damage = random.randint(1,2)
        print (name+" gains",damage,"HP!")
        health = health+damage
    else:
        print("NO NO BIG BOI")

    print (eName+"'s turn!")
    input("Press enter to see "+eName+"'s actions!")
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
