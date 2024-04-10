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
    limit_round = 25
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
    return False, rounds #if rounds > rounds limit then NPC LOST!

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


 #Funcao a ser optimizada: Numero de vitorias em X batalhas.
######################### INPUTS ##########################
# [%] of win desired
goal = 75    
#Number of fights the character and NPC will fight, the higher the more precise the output is.
battle_number = 2000
#Popolation size
pop_size = 100
#Generations
gen = 300
# [%] of elitism considered
elitism = 5
###########################################################
# Player Character who is going to be the reference
ref = char(15, 3 ,5 ,8 ,6)
# Actual desired number of wins to be considered in the algorithm.
true_goal = int(battle_number * goal/100)  
#print("true goal is:", true_goal)
# Number of individuals that'll be kept through a generation due to elitism
elite_num = int(elitism * pop_size/100)  
#print("individuals in elite is:", elite_num)
# Initial Population 
pop = create_population(pop_size,ref.lvl)
# Initialization 
all_pop = [[] for i in range(gen)] #list of all populations (one for each generation)
new_pop = []
used_parent = []
GA = GAtoolbox()
#TODO: A list to save all results of some generations?
#TODO: A list to save how many rounds each battle took? Or maybe just the average?

#AlgoFLOW #TODO: O algoritmo ta configurado pro melhor boneco ser o que venceu mais. nao e isso que eu quero! a fitness function e a distancia do meu alvo de vitorias!
for g in range(gen):
    #print("======================")
    #print("Gen ", g+1)
    result = tourney(battle_number, pop, ref)
    #print("result antes:" , result)
    for i in range(len(result)):
        result[i] = abs(result[i] - true_goal)
    #print("result com true goal:", result)
    sorted_indices = sorted(range(len(result)), key=lambda i: result[i], reverse=False) #This gives a list with the sorted indexes of a result list -> first_result[sorted_indices[0] is the individual with the most wins]
    saved_std_indices = sorted_indices.copy()
    #print("indeces de result ordenado ", sorted_indices)
    #print("saved sorted indices", saved_std_indices)
    
    #Separate Elite
    for j in range(elite_num):
        #print("---elite---")
        #print(pop[sorted_indices[j]])
        new_pop.append(pop[sorted_indices[j]])

    #print("how many individuals in elite: ", len(new_pop))
    #Do crossover
    """Individuals randomly selected from the group that was not part of the elite"""
    #for k in range(0,pop_size-elite_num,1):
    while (len(new_pop) < pop_size):
        """um while loop que vai continuar enquanto o tamanho de new_pop for menor que o requisitado
        porem, se a qtd de individuos que falta for 1, sorteia um individuo e fecha o loop"""
        #print("---crossover---")
        #print("tamanho da pop: ", len(new_pop))
        if pop_size-len(new_pop)==1:
            new_pop.append(pop[rd.randint(0,pop_size-1)])
            #print("tamanho da pop: ", len(new_pop))
            break

        if (elite_num == (len(sorted_indices)-1)):
            break

        parent1 = sorted_indices[rd.randint(elite_num,len(sorted_indices)-1)]
        used_parent.append(parent1)
        sorted_indices.remove(parent1)

        parent2 = sorted_indices[rd.randint(elite_num,len(sorted_indices)-1)]
        used_parent.append(parent2)
        sorted_indices.remove(parent2)
        
        parent1 = GA.char2gene(pop[parent1])
        #print("parent1 tam: ", len(parent1))
        parent2 = GA.char2gene(pop[parent2])
        #print("parent2 tam: ", len(parent2))

        children = GA.crossover(parent1, parent2)
       
        for child in children:
            child = GA.gene2char(child)
            child = char(ref.lvl, child[0], child[1], child[2], child[3])
            new_pop.append(child)         

    #Do Mutation for those that are not elites
    for k in range(elite_num,pop_size-1):
        indiv = new_pop[k]
        #print("b4")
        #print(indiv)
        indiv = GA.char2gene(indiv)
        indiv = GA.mutation(indiv)
        indiv = GA.gene2char(indiv)
        indiv = char(ref.lvl, indiv[0], indiv[1], indiv[2], indiv[3])
        new_pop[k] = indiv
        #print("after")
        #print(indiv)
        #print()

    #Set new_pop as pop and reset new_pop
    pop = new_pop
    new_pop = []
    
    #print("saved sorted indices", saved_std_indices)


    #if (g-1) in gen2print: 
    print("============RESULTS============")
    print("GENERATION: ", g+1)
    print()
    for i in range(2):
        print(pop[saved_std_indices[i]])
        print("Distance from goal: ",result[saved_std_indices[i]])    
        print()  

with open("characters.txt", "w") as f:
    for i,character in enumerate(pop):
        f.write("Distance from goal: " + str(result[saved_std_indices[i]]) + "\n")
        f.write(str(character) + "\n")
        f.write("----------------------------- \n\n")


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

