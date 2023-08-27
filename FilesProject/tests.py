import random as rd
import numpy as np
#-----------------------------------
import GameSystem as gs
import Character as char
import GAtoolbox as GAtoolbox


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

ref = char(1, 5, 14, 4, 17)

print(ref)

offspring1 = []
offspring2 = []
A = [0,1,2,3]
for i in range(2): 
    i1 = rd.choice(A)
    if (i1 not in offspring1): offspring1.append(i1)
for element in A: