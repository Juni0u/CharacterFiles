from Game_system import Game_system as gs
from Game_system import Character as char
from Game_system import GAtoolbox
import random as rd
import numpy as np

import random

"""new_list = []
result = [11, 22, 33, 44, 55, 66, 77, 88, 99, 100]
sorted_indices = sorted(range(len(result)), key=lambda i: result[i], reverse=True) 

for i in range(5):
    print("si ", sorted_indices)
    parent1 = sorted_indices[rd.randint(0,len(sorted_indices)-1)]
    new_list.append(parent1)
    sorted_indices.remove(parent1)
    print(parent1)
"""

teste = [200, 100, 0, 50, 150]
print("teste antes: ", teste)
for i in range(len(teste)):
    teste[i] = abs(teste[i] - 100)

print("teste depois: ", teste)

