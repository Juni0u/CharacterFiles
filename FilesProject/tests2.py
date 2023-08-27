import random as rd
from GameSystem import GameSystem as gs
from GameSystem import Character as char
from GAtoolbox import GAtoolbox as GAtb


"""A = [34, 72, 10, 53, 86, 18, 95, 41, 99, 12, 78, 68, 32, 56, 62, 3, 21, 79, 46, 14, 65, 23, 8, 44, 90, 59, 48, 33, 30, 71, 24, 77, 64, 29, 92, 94, 81, 26, 6, 96, 45, 9, 84, 58, 49, 47, 11, 55, 5, 75, 82, 16, 76, 31, 63, 60, 2, 87, 80, 85, 37, 91, 73, 35, 70, 25, 67, 40, 13, 88, 97, 69, 0, 50, 7, 4, 17, 61, 22, 93, 36, 51, 83, 74, 42, 54, 27, 57, 1, 20, 66, 38, 43, 39, 19, 28, 89, 98, 15, 52]
GA = GAtoolbox(start_pop=A, wins_goal=50, duration_goal=3, battle_number= 10,
               pop_size=100, gen=1,weight_wins=1,weight_duration=0)
"""

ref = char(3 ,5 ,7 ,8, 16)
ref2 = char(8, 7, 5, 3, 16)
GA = GAtb(50,10,1000,500,300)

print(GA.create_population(15))