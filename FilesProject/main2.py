from FilesProject.GAtoolbox import Game_system
from FilesProject.GAtoolbox import Character as char
from FilesProject.GAtoolbox import GAtoolbox
from FilesProject.GAtoolbox import parameter as param
import random as rd
import numpy as np

GS = Game_system()

# Player Character who is going to be the reference
ref = char(1, 5, 14, 4,17)

GA = GAtoolbox(wins_goal=75,duration_goal=7,
               battle_number=1500,gen=300,pop_size=100,
               weight_duration=0,weight_wins=1)

#### This will be inside the start the algorithm function
pop = GA.evolve(ref)

with open("characters.txt", "w") as f:
    for i,individual in enumerate(pop):
       # print(individual.character)
        f.write("ID: " + str(individual.id) + "\n")
        f.write("Fitness: " + str(individual.fit) + "\n")
        f.write(str(individual.character) + "\n")
        f.write("----------------------------- \n\n")

#TODO:
""" 1. Individuos com mesmo ID mas atributos diferentes. (Olhar como os IDs estao sendo colocados)
    2. Individuos com fitness 99999 na populacao. Completamente zuados. Sera que e da mutacao? Talvez seja. Verificar."""