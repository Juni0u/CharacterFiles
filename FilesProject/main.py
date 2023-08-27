from FilesProject.GAtoolbox import Game_system
from FilesProject.GAtoolbox import Character as char
from FilesProject.GAtoolbox import GAtoolbox
from FilesProject.GAtoolbox import parameter as param
import random as rd
import numpy as np

#smol change 


def battle (player, NPC: object):
    """This function executes the battle itself.\n 
    I = Player and NPC that will be fighting\n
    O = True for NPC WIN"""
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
    rounds_sum = 0
    result = [] #list that saves how many wins each individual of 'pop' got.
    rounds_avg = [] #list that saves the AVG duration of battles each individual of 'pop' got.
    #rounds = [[] for i in range(pop_size)] #list of how many rounds each battle took to end
    for k, enemy in enumerate(pop):
        #print()
        #print("enemy ", k)
        for i in range(0,battle_number):
            battle_result,round_qty = battle(ref,enemy)
            #print("battle ",i," - result = ",battle_result)
            rounds_sum += round_qty
            if battle_result:
                wins += 1
        result.append(wins)
        rounds_avg.append(rounds_sum/battle_number)
        wins = 0 
        rounds_sum = 0
    return result, rounds_avg

 #Funcao a ser optimizada: Numero de vitorias em X batalhas.
######################### INPUTS ##########################
# [%] of NPC win desired
wins_goal = 10
# how many rounds should the battle have
duration_goal = 5 
#Number of fights the character and NPC will fight, the higher the more precise the output is.
battle_number = 10
#Popolation size
pop_size = 10
#Generations
gen = 1
# [%] of elitism considered
elitism = 10
###########################################################
# Player Character who is going to be the reference
ref = char(3 ,5 ,8 ,6, 15)
# Actual desired number of wins to be considered in the algorithm.
wins_true_goal = int(battle_number * wins_goal/100)  
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
GA = GAtoolbox(start_pop=pop,
               wins_goal=wins_goal,
               duration_goal=duration_goal,
               battle_number=battle_number,
               gen=gen,
               pop_size=pop_size,
               weight_duration=0.5,
               weight_wins=0.5)
GS = Game_system()

#TODO: A list to save all results of some generations?
#TODO: A list to save how many rounds each battle took? Or maybe just the average?

for g in range(gen):
    #print("======================")
    print("Gen ", g+1)
    result, rounds = tourney(battle_number, pop, ref)
    for i in range(len(result)):
        #pop_fitness.append(GA.fitness_function(wins=result[i],avg_dur=rounds[i]))
        

    GA.selection(pop_fitness=pop_fitness)
    
    
    sorted_indices = sorted(range(len(pop_fitness)), key=lambda i: pop_fitness[i], reverse=False) #This gives a list with the sorted indexes of a result list -> first_result[sorted_indices[0] is the individual with the most wins]
    #saved_std_indices = sorted_indices.copy()
        
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
            child = char(child[0], child[1], child[2], child[3], ref.lvl)
            new_pop.append(child)         

    #Do Mutation for those that are not elites
    for k in range(elite_num,pop_size-1):
        indiv = new_pop[k]
        #print("b4")
        #print(indiv)
        indiv = GA.char2gene(indiv)
        indiv = GA.mutation(indiv)
        indiv = GA.gene2char(indiv)
        indiv = char(indiv[0], indiv[1], indiv[2], indiv[3], ref.lvl)
        new_pop[k] = indiv
        #print("after")
        #print(indiv)
        #print()

    #Set new_pop as pop and reset new_pop
    pop = new_pop
    new_pop = []
    
    #print("saved sorted indices", saved_std_indices)


    #if (g-1) in gen2print: 
"""    print("============RESULTS============")
    print("GENERATION: ", g+1)
    print()
    for i in range(2):
        print(pop[saved_std_indices[i]])
        print("Distance from goal: ",result[saved_std_indices[i]])    
        print() """

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

