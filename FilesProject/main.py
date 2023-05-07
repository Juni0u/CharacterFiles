from Game_system import Game_system as gs
from Game_system import Character as char
from Game_system import toolbox
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

def battle (player,NPC):
    """This function executes the battle itself. 
    Input: Player and NPC that will be fighting
    Output: True for NPC WIN"""
    limit_round = 30
    rounds = 0
    player.reset_hp()
    NPC.reset_hp()

    while rounds < limit_round:
        if player.attack(NPC):
            NPC.update_hp(-player.pdr)
            if NPC.hp < 1:
                return False
        if NPC.attack(player):     
            player.update_hp(-NPC.pdr)
            if player.hp < 1:
                return True
        rounds += 1
    return True


 #Funcao a ser optimizada: Numero de vitorias em X batalhas.
## INPUTS

# [%] of win desired
goal = 60             
# Player Character who is going to be the reference
ref = char(15, 1, 5, 12 , 4)

#Number of fights the character and NPC will fight, the higher the more precise the output is.
battle_number = 10
#Actual desired number of wins to be considered in the algorithm.
true_goal = int(battle_number * goal/100)  

#Initial Population 
pop = create_population(100,ref.lvl)

#Battles of the first population
"""In the evalution, each member of the population will fight the
reference character [battle_number] times"""
wins = 0
result = [] #list that saves how many wins each individual of 'pop' got.
for enemy in pop:
    for i in range(0,battle_number):
        if battle(ref,enemy):
            wins += 1
    result.append(wins)
    wins = 0 

#Getting how far from the goal each individual is
tgoal_diff = []
for each in result:
    tgoal_diff.append(abs(each-true_goal))

"""for i,each in enumerate(result):
    if each > true_goal:
        print("WON ",each,"times.")
        print(pop[i])
        print("=======")"""

#TODO CONVERTER PARA BINARIO E APLICAR MUTACAO E CROSSOVER
tb = toolbox(5)
print(ref)
print("============")
genes = tb.char2gene(ref)
print("genes origin",genes)
print("origin converted", tb.gene2char(genes))
#NO FINAL VERIFICAR SE É UM PERSONAGEM VÁLIDO

#teste = [4,2,4,-3,1]
# 4,1,3,0,2
#print(np.argsort(teste))

#00001 00101 01100 00100

mutation = tb.mutation(genes,0.1)
print("genesmutated",mutation)
print("mutation converted", tb.gene2char(mutation))

