from Game_system import Game_system as gs
from Game_system import Character as char
from Game_system import GAtoolbox
import random as rd
import numpy as np

import random

new_list = []
result = [11, 22, 33, 44, 55, 66, 77, 88, 99, 100]
sorted_indices = sorted(range(len(result)), key=lambda i: result[i], reverse=True) 

for i in range(5):
    print("si ", sorted_indices)
    parent1 = sorted_indices[rd.randint(0,len(sorted_indices)-1)]
    new_list.append(parent1)
    sorted_indices.remove(parent1)
    print(parent1)
