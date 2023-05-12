from Game_system import Game_system as gs
from Game_system import Character as char
from Game_system import GAtoolbox
from Game_system import parameter as param
import random as rd
import numpy as np
 
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

def battle (player, NPC):
    """This function executes the battle itself. 
    Input: Player and NPC that will be fighting
    Output: True for NPC WIN"""
    limit_round = 10
    rounds = 0
    player.reset_hp()
    NPC.reset_hp()

    while rounds < limit_round:
        if player.attack(NPC):
            NPC.update_hp(-player.pdr)
            if NPC.hp < 1:
                return False, rounds
        if NPC.attack(player):     
            player.update_hp(-NPC.pdr)
            if player.hp < 1:
                return True, rounds
        rounds += 1
    return True, rounds

def tourney (pop_size, battle_number, pop, ref):
    """INPUTS: pop_size, qtd of battles against each NPC, population of enemies, reference player
    OUTPUT: List of how many wins each enemy got, List of how many rounds each fight took to end"""
    wins = 0
    result = [] #list that saves how many wins each individual of 'pop' got.
    rounds = [[] for i in range(pop_size)] #list of how many rounds each battle took to end
    for k, enemy in enumerate(pop):
        for i in range(0,battle_number):
            battle_result,round_qty = battle(ref,enemy)
            rounds[k].append(round_qty)
            if battle_result:
                wins += 1
        result.append(wins)
        wins = 0 
    return result, rounds


 #Funcao a ser optimizada: Numero de vitorias em X batalhas.
######################### INPUTS ##########################
# [%] of win desired
goal = 60    
#Number of fights the character and NPC will fight, the higher the more precise the output is.
battle_number = 500
#Popolation size
pop_size = 500
#Generations
gen = 1000
###########################################################
# Player Character who is going to be the reference
ref = char(15, 3 ,5 ,9 ,6)
#Actual desired number of wins to be considered in the algorithm.
true_goal = int(battle_number * goal/100)  
# Initial Population 
pop = create_population(pop_size,ref.lvl)
# Initialization 
all_pop = [[] for i in range()] #list of how many rounds each battle took to end


#Battles of the first population
first_result, first_rounds = tourney(pop_size, battle_number, pop, ref)
print(first_result)



#Getting how far from the goal each individual is
"""tgoal_diff = []
for each in result:
    tgoal_diff.append(abs(each-true_goal))

print(tgoal_diff)"""

"""for i,each in enumerate(result):
    if tgoal_diff[i] < 300:
        print("WON ",each,"times.")
        print(pop[i])
        print("=======")"""

