from Game_system import Game_system as gs
from Game_system import Character as char
from Game_system import GAtoolbox
import random as rd
import numpy as np

import random

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

def tourney (battle_number, pop, ref):
    """INPUTS: pop_size, qtd of battles against each NPC, population of enemies, reference player
    OUTPUT: List of how many wins each enemy got, List of how many rounds each fight took to end"""
    wins = 0
    result = [] #list that saves how many wins each individual of 'pop' got.
    #rounds = [[] for i in range(pop_size)] #list of how many rounds each battle took to end
    for k, enemy in enumerate(pop):
        for i in range(0,battle_number):
            battle_result,round_qty = battle(ref,enemy)
            #rounds[k].append(round_qty)
            if battle_result:
                wins += 1
        result.append(wins)
        wins = 0 
    return result#, rounds

ref = char(15, 3, 5, 8, 6)
build = char(15, 5, 5, 6, 6)

goal = 75    
battle_number = 1000
true_goal = int(battle_number * goal/100)  

result = tourney(battle_number,[build],ref)

print(result[0]-true_goal)

for each in result:
    print(abs(each-true_goal))
