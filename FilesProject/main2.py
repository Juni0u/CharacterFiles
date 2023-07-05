from Game_system import Game_system
from Game_system import Character as char
from Game_system import GAtoolbox
from Game_system import parameter as param
import random as rd
import numpy as np

GS = Game_system()

# Player Character who is going to be the reference
ref = char(3 ,5 ,8 ,6, 15)

GA = GAtoolbox(wins_goal=10,duration_goal=5,
               battle_number=10,gen=1,pop_size=100,
               weight_duration=0.5,weight_wins=0.5)

#### This will be inside the start the algorithm function
GA.evolve(ref)


