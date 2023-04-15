from Game_system import Game_system as gs
from Game_system import Character as char
import random as rd
 
def create_population (n,lvl):
    """Creates the population of n individuals of level lvl"""
    players = []
    for i in range (0,n):
        pdr = rd.randint(0, lvl+1)
        pre = rd.randint(0, lvl+1-pdr) 
        defe = rd.randint(0, lvl+1-pdr-pre)
        con = (lvl+1-pdr-pre-defe)
        players.append(char(lvl,pdr+1,pre+1,defe+1,con+3))
    return players

def battle (player,NPC):
    """This function executes the battle itself. It returns the index
    of the winner in the input list.
    Input: Player and NPC that will be fighting
    Output: True for NPC WIN"""
    finish = False
    while finish==False:
        if player.attack(NPC):
            NPC.update_hp(-player.pdr)
            if NPC.hp < 1:
                return False
        if NPC.attack(player):     
            player.update_hp(-NPC.pdr)
            if player.hp < 1:
                return True


 #Funcao a ser optimizada: Numero de vitorias em X batalhas.
## INPUTS

# [%] of win desired
goal = 60             
# Player Character who is going to be the reference
ref = char(15, 1, 5, 12 , 4)

#Number of fights the character and NPC will fight, the higher the more precise the output is.
battle_number = 5
#Actual desired number of wins to be considered in the algorithm.
true_goal = int(battle_number * goal/100)  

#Initial Population 
pop = create_population(10,ref.lvl)

#Evaluation of the first population
"""In the evalution, each member of the population will fight the
reference characters [battle_number] times"""
wins = 0
result = [] #list that saves how many wins each individual of 'pop' got.
for enemy in pop:
    for i in range(0,battle_number):
        if battle(ref,enemy):
            wins += 1
    result.append(wins)
    wins = 0 

for each in result:
    print(each)

