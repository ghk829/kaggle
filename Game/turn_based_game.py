#This version is made for AI. Copyrighted: NickandNicksGaming LLC
#Date modified = 3/29/2013
#Version: Beta 1.4

from sys import exit
import os
import os.path
import pickle

global options
options = ["BUILD (B)", "RESEARCH (R)", "TRAIN (T)", "DEPLOY (D)", "END (E)", "QUIT (Q)"]

def Won(player, reason):
    print(player.name+" wins, %s" %reason)
    won = True
    return won

class player(object):

    def __init__(self, name, color):
        self.name = name
        self.color = color

        self.Mill = {'price':10, 'num':0, 'desc':"Collects 5 FOOD every turn with bonus."}
        self.Quarry = {'price':15, 'num':0, 'desc':"Collects 5 GOLD every turn with bonus."}
        self.LumberYard = {'price':15, 'num':1, 'desc':"Collects 5 WOOD every turn with bonus."}
        self.factory = {'price':50, 'num':0, 'desc':"Collects 20 of EVERY resource each turn NO BONUS."}
        self.Wonder = {'price':1000, 'num':0, 'desc':"Wins you the game."}

        self.spy = {'price':15, 'num':0, 'desc':"Lets you see opponent's resources, buildings, and advances."}
        self.raider = {'price':25, 'num':0, 'desc':"Destroys one of the most common building in enemy's base"}
        self.thief = {'price':20, 'num':0, 'desc':"Steals 5 of an opponents resource of your choice"}

        #self.sharperaxes = {'price':2, 'level':1, 'desc':"}        Dictionaries for advances. to add. too lazy.
        
        self.gold = {'num': 5, 'desc':"Used to research new advances for faster resource collection."}
        self.wood = {'num': 5, 'desc':"Used to build buildings."}
        self.food = {'num': 5, 'desc':"Used to train units."}
        
        #self.rescources = {'GOLD':5, 'WOOD':10, 'FOOD':5}
        self.resources = {'GOLD':self.gold, 'WOOD':self.wood, 'FOOD':self.food}
        self.buildings = {'MILL':self.Mill, 'QUARRY':self.Quarry, 'LUMBER YARD':self.LumberYard, 'FACTORY':self.factory, 'WONDER':self.Wonder}
        self.advances = {'SHARPER AXES':1, 'CROP ROTATION':1, 'SHARPER PICKS':1}
        self.units = {'SPY': self.spy, 'RAIDER':self.raider, 'THIEF':self.thief}

class AI(player):


    def turn(self, next_player):
        self.resources["FOOD"]["num"]+=self.buildings["MILL"]["num"]*5*self.advances['CROP ROTATION']+(self.buildings["FACTORY"]["num"]*20)
        self.resources["WOOD"]["num"]+=self.buildings["LUMBER YARD"]["num"]*5*self.advances['SHARPER AXES']+(self.buildings["FACTORY"]["num"]*20)
        self.resources["GOLD"]["num"]+=self.buildings["QUARRY"]["num"]*5*self.advances['SHARPER PICKS']+(self.buildings["FACTORY"]["num"]*20)
        food_done = False
        while food_done == False:
            if self.resources["FOOD"]["num"] >= 25:
                self.units["RAIDER"]["num"]+=1
                self.resources["FOOD"]["num"]-=25

            while self.units["RAIDER"]["num"] > 0:

                list1 = []
                for i in next_player.buildings:
                    list1.append((next_player.buildings[i]["num"], i))
                
                destroyed = max(list1)
                if destroyed[0]>0:
                    next_player.buildings[destroyed[1]]["num"]-=1
                    print("Enemy %s destroyed!" %destroyed[1])
                    self.units["RAIDER"]["num"]-=1
                else:
                    print("Nothing to destroy!")
                    break

            food_done = True
        wood_done = False

        while wood_done == False:
            if self.resources["WOOD"]["num"] >= 1000:
                self.buildings["WONDER"]["num"]+=1
                self.resources["WOOD"]["num"] -= 1000
                won = Won(self, "Alpha built a WONDER")
                break

            elif self.resources["WOOD"]["num"] >= 15:
                if self.buildings["LUMBER YARD"]["num"] == self.buildings["QUARRY"]["num"]:
                    if self.buildings["MILL"]["num"] < self.buildings["LUMBER YARD"]["num"]:
                        self.buildings["MILL"]["num"]+=1
                        self.resources["WOOD"]["num"]-=10
                    else:
                        self.buildings["LUMBER YARD"]["num"]+=1

                else:
                    min_build = min(self.buildings["LUMBER YARD"], self.buildings["QUARRY"])
                    if self.buildings["MILL"]["num"] == min_build["num"]:
                        self.buildings["MILL"]["num"]+=1
                        self.resources["WOOD"]["num"]-=10
                    else:
                        min_build["num"]+=1
                        self.resources["WOOD"]["num"]-=15

            elif self.resources["WOOD"]["num"]<15 and self.resources["WOOD"]>=10:
                min_build = min(self.buildings["LUMBER YARD"]["num"], self.buildings["QUARRY"]["num"], self.buildings["MILL"]["num"])
                if self.buildings["MILL"]["num"] == min_build:
                    self.buildings["MILL"]["num"]+=1
                    self.resources["WOOD"]["num"]-=10
                    wood_done =True
                else:
                    wood_done = True

            else:
                wood_done = True
                        
            gold_done = False
            
            while gold_done == False:
                
                if self.advances["SHARPER AXES"]== self.advances["SHARPER PICKS"] == self.advances["CROP ROTATION"]:
                    if self.resources["GOLD"]["num"] >= (self.advances["SHARPER AXES"]*2)**2:
                        self.resources["GOLD"]["num"]-=(self.advances["SHARPER AXES"]*2)**2
                        self.advances["SHARPER AXES"]+=1

                    else:
                        gold_done = True

                elif self.advances["SHARPER PICKS"] == self.advances["CROP ROTATION"]:
                    if self.resources["GOLD"]["num"] >= (self.advances["CROP ROTATION"]*2)**2:                 
                        self.resources["GOLD"]["num"]-=(self.advances["CROP ROTATION"]*2)**2
                        self.advances["CROP ROTATION"]+=1
                        
                    else:
                        gold_done = True

                else:
                    if self.resources["GOLD"]["num"] >= (self.advances["SHARPER PICKS"]*2)**2:     
                        self.resources["GOLD"]["num"]-=(self.advances["SHARPER PICKS"]*2)**2
                        self.advances["SHARPER PICKS"]+=1
                        
                    else:

                        gold_done = True
                    
                
        
                

        



def start():
    start = False
    while start == False:
        start_option = raw_input("New game (N) or load a game (L)?: ").upper()
        
        if start_option == "NEW GAME" or start_option == "N":
            os.system('cls')        #clears screen
            os.system('color c')    #Light red
            
            player1 = player(raw_input("What is your name Player 1?: ").upper(), 'a')   #Light green
            player2 = AI("Alpha", 0)
            
            first, second = player1, player2
            Won = False
            start = True
            turn = 0
            
        elif start_option == "LOAD" or start_option == "L":

            raw_filenames = os.listdir(".\Saves")

            save_files = []
            for name in raw_filenames:

                if name.endswith('.pkl'):
                    save_files.append(os.path.join(".\Saves", name))

            if len(save_files) <1:
                print("No save files!")

            else:
                os.system('cls')
                save_files.reverse()
                print("Save Games:\n")
                for name in save_files:
                    print(name[8:][:-4]+"\n")

                save_option =raw_input("What game would you like to load? (or BACK (B)): ").upper()
                if save_option == "B" or save_option == "BACK":
                    os.system('cls')
                else:
                    try:
                        opened_file = open('.\Saves\\'+save_option+'.pkl', 'rb')
                        data = pickle.load(opened_file)
                        
                        second, first, Won, turn = data
                        start = True
                    except Exception:
                        os.system('cls')
                        print("Not a valid name\n")

        else:
            print "try again\n"
            
    while Won==False:
        first, second, Won, turn = play_turn(player1, player2, Won, turn)
        player2.turn(player1)
        
    raw_input("Hit enter to close. ")


def play_turn(current_player, next_player, Won, turn1):

    turn1 +=1
    os.system('cls')
    os.system('color %s' %current_player.color)

    raw_input(current_player.name+", hit enter to start turn.")

    turn = 1
    
    if current_player.name[-1] == 'S': #Just some proper grammer
        print "\nIt is "+current_player.name+"' Turn\n"
    else:
        print "\nIt is "+current_player.name+"'s Turn\n"

    print "FOOD from MILLs:",current_player.buildings["MILL"]["num"]*5*current_player.advances['CROP ROTATION']
    print "WOOD from LUMBER YARDs:",current_player.buildings["LUMBER YARD"]["num"]*5*current_player.advances['SHARPER AXES']
    print "GOLD from QUARRYs:",current_player.buildings["QUARRY"]["num"]*5*current_player.advances['SHARPER PICKS']

    if current_player.buildings["FACTORY"]["num"] >0:
        print "WOOD, FOOD, and GOLD from FACTORIES:",current_player.buildings["FACTORY"]["num"]*20
    
    current_player.food["num"]+=current_player.buildings["MILL"]["num"]*5*current_player.advances['CROP ROTATION']+(current_player.buildings["FACTORY"]["num"]*20)
    current_player.wood["num"]+=current_player.buildings["LUMBER YARD"]["num"]*5*current_player.advances['SHARPER AXES']+(current_player.buildings["FACTORY"]["num"]*20)
    current_player.gold["num"]+=current_player.buildings["QUARRY"]["num"]*5*current_player.advances['SHARPER PICKS']+(current_player.buildings["FACTORY"]["num"]*20)

    research = False

    while turn and Won==False:

        if current_player.buildings["WONDER"]["num"]>0:
            Won = True

        if Won == True:
            raw_input(str(current_player.name)+" Won! ")
            return(0, 0, Won)
        
        print "\nBuildings:"

        for i in current_player.buildings.keys():                      #Lists the player's buildings
            print str(i)+" -", current_player.buildings[i]["num"]

        print "\nAdvances:"
        
        for i in current_player.advances:                          #Lists the player's units
            print str(i)+" -", current_player.advances[i]
            
        print "\nResources:"
        
        for i in current_player.resources:
            print str(i)+" -", current_player.resources[i]["num"]

        print "\nUnits:"
        
        for i in current_player.units:
            print str(i)+" -", current_player.units[i]["num"]


        print "\nYour options are:\n",        #list options for the players turn.
        for i in options:
            if i == options[-1]:
                print "and " + i +"."
            else:
                print i + ",",
            
        print "\n"
        
        choice = raw_input("What do you want to do?: ").upper()
        print "\n"
        
        if choice == "BUILD" or choice == "B":          #Build buildings to help supply resources
            print "WOOD: "+str(current_player.resources["WOOD"]["num"])+"\n"
            for keys in current_player.buildings.keys():
                print keys+"----------------"
                print "Current number: "+str(current_player.buildings[keys]["num"])
                print "WOOD required to build: "+str(current_player.buildings[keys]["price"])
                print current_player.buildings[keys]["desc"]
                print "\n"

            build_choice = raw_input("What would you like to build?: ").upper()
            print "\n"
            
            if build_choice in current_player.buildings:
                if current_player.resources["WOOD"]["num"]>=current_player.buildings[build_choice]["price"]:
                    current_player.resources["WOOD"]["num"]-=current_player.buildings[build_choice]["price"]
                    current_player.buildings[build_choice]["num"]+=1
                    print "Current WOOD: "+str(current_player.resources["WOOD"]["num"])
                    print "Current number of "+str(build_choice)+":", current_player.buildings[build_choice]["num"]
                else:
                    print "Not enough WOOD!"
            else:
                print "Please choose a valid option."

            raw_input("\nPress enter to continue ")

        elif choice == "RESEARCH" or choice == "R":     #Research advanced ways to gather resources
            print "GOLD: "+str(current_player.resources["GOLD"]["num"])+"\n"
            if research == False:
                for keys in current_player.advances.keys():
                    print keys+"----------------"
                    print "Current level: "+str(current_player.advances[keys])
                    print "GOLD required to upgrade: "+str((current_player.advances[keys]*2)**2)
                    print "\n"

                research_choice = raw_input("What would you like to upgrade?: ").upper()
                print "\n"
                if research_choice in current_player.advances:
                    if current_player.resources["GOLD"]["num"]>=(current_player.advances[research_choice]*2)**2:
                        current_player.resources["GOLD"]["num"]-=(current_player.advances[research_choice]*2)**2
                        current_player.advances[research_choice]+=1
                        print "Current GOLD: "+str(current_player.resources["GOLD"]["num"])
                        print "Current",research_choice,"level:", current_player.advances[research_choice]
                        #research = True
                    else:
                        print "Not enough GOLD!"
                else:
                    print "Please choose a valid option."
            elif research:
                print "You can only research one thing per turn!"

            raw_input("\nPress enter to continue ")

        elif choice == "TRAIN" or choice == "T":
            print "FOOD: "+str(current_player.resources["FOOD"]["num"])+"\n"
            for keys in current_player.units.keys():
                print keys+"----------------"
                print "FOOD required to use: "+str(current_player.units[keys]["price"])
                print current_player.units[keys]["desc"]
                print "\n"

            train_choice = raw_input("What would you like to train?: ").upper()
            if train_choice in current_player.units:
                if current_player.resources["FOOD"]["num"]>=current_player.units[train_choice]["price"]:
                    current_player.resources["FOOD"]["num"]-=current_player.units[train_choice]["price"]
                    current_player.units[train_choice]["num"]+=1
                    print "Current FOOD: "+str(current_player.resources["FOOD"]["num"])
                    print "Current "+train_choice+":",current_player.units[train_choice]["num"]
                else:
                    print "Not enough FOOD!"
            else:
                print "Please choose a valid option."

            raw_input("\nPress enter to continue ")

        elif choice == "DEPLOY" or choice == "D":
            for i in current_player.units:
                print i, current_player.units[i]["num"]

            deploy_choice = raw_input("What would you like to deploy?: ").upper()
            print "\n"
            
            if deploy_choice in current_player.units and current_player.units[deploy_choice]["num"]>0:
                if deploy_choice == "SPY":
                    print "*REPORT*\n*ENEMY HAS*\n"
                    for i in next_player.buildings:
                        print i, next_player.buildings[i]["num"]
                    for i in next_player.resources:
                        print i, next_player.resources[i]["num"]
                    for i in next_player.advances:
                        print i, next_player.advances[i]
                    print "/n*END REPORT*"

                    current_player.units["SPY"]["num"]-=1

                elif deploy_choice == "RAIDER">0:
                    list1 = []
                    for i in next_player.buildings:
                        list1.append((next_player.buildings[i]["num"], i))
                    
                    destroyed = max(list1)
                    if destroyed[0]>0:
                        next_player.buildings[destroyed[1]]["num"]-=1
                        print "Enemy %s destroyed!" %destroyed[1]
                        current_player.units["RAIDER"]["num"]-=1
                    else:
                        print "Nothing to destroy!"

                elif deploy_choice == "THIEF">0:
                    available_resources = []
                    for i in next_player.resources:
                        if next_player.resources[i]["num"]>=5:
                            available_resources.append(i)
                            
                    if len(available_resources)>0:
                        print "You could steal 5 of:"
                        for i in available_resources:
                            print i
                    else:
                        print "Nothing to steal!"

                    succeded = False
                    if len(available_resources)>0:
                        while succeded == False:
                            steal = raw_input("What would you like to steal?: ").upper()
                            if steal in available_resources:

                                next_player.resources[steal]["num"]-=5
                                current_player.resources[steal]["num"]+=5
                                succeded = True
                                
                            else:
                                print "Error"

                            if succeded == True:
                                current_player.units["THIEF"]["num"]-=1

            raw_input("\nPress enter to continue ")


        elif choice == "END" or choice == "E":
            turn = False
            everything = [current_player, next_player, Won, turn]

            output = open('.\Saves\\'+current_player.name[:6]+next_player.name[:6]+str(turn1)+'.pkl', 'wb')

            pickle.dump(everything, output, -1)

            output.close()
            
        elif choice == "QUIT" or choice == "Q":
            exit("QUITTING")


        else:
            print "Not an option"



    if turn==0:
        raw_input("\nHit enter to end your turn. ")
        return(next_player, current_player, Won, turn1)



if __name__ == '__main__':
    start()
