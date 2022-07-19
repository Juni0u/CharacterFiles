from Character import Character as char
from BattleSim import BattleSim as bs
import random as rd
# lvl, pdr, pre, def, con
Tyr = char(13, 2, 3, 7, 7)
Akin = char(15, 2, 5, 7, 7)
Pucky = char(10, 2, 3, 5, 7)
Akane = char(5, 2, 2, 3, 4)

TyrList = [Tyr.lvl, Tyr.pdr, Tyr.pre, Tyr.defe, Tyr.con, Tyr.lvlbonus]
AkinList = [Akin.lvl, Akin.pdr, Akin.pre, Akin.defe, Akin.con, Akin.lvlbonus]
AkaneList = [Akane.lvl, Akane.pdr, Akane.pre, Akane.defe, Akane.con, Akane.lvlbonus]

TyrAns = [13, 2, 3, 7, 7, 9]
AkinAns = [15, 2, 5, 7, 7, 11]
PuckyAns = None
AkaneAns = [5, 2, 2, 3, 4, 3]

#%% Testing object creation
for i,element in enumerate(TyrList):
    assert element is TyrAns[i],  print("Error in Tyr!")
    
for i,element in enumerate(AkinList):
    assert element is AkinAns[i],  print("Error in Akin!")
    
assert Pucky is None, print("Error in pucky!") 

for i,element in enumerate(AkaneList):
    assert element is AkaneAns[i],  print("Error in Akane!")

print("No errors found in object creation :)")
#%% Test rolls
for k in range(1,10000):
    for i in range(1,4):
        assert Tyr.get_atk(bs.roll_dices())[i] < 7, print("Dice value is wrong! Its bigger than 6!")
        assert Akin.get_atk(bs.roll_dices())[i] < 7, print("Dice value is wrong! Its bigger than 6!")
        assert Akane.get_atk(bs.roll_dices())[i] < 7, print("Dice value is wrong! Its bigger than 6!")

print("No problem in atk rolls! :)")

#%% Test Def stat
assert Tyr.get_def() == 26, print("Tyr DEF is wrong!")
assert Akin.get_def() == 28, print("Akin DEF is wrong!")
assert Akane.get_def() == 16, print("Akane DEF is wrong!")

print("No problem in def rolls! :)")

#%% Test HP reduction and SUM
Tyr.update_hp(-3)
assert Tyr.hp == 4, print("HP do Tyr tinha que ser 4")

Tyr.reset_hp()
assert Tyr.hp == 7, print("HP do Tyr tinha que ser 7")

Akin.update_hp(2)
assert Akin.hp == 9, print("HP do Akin tinha que ser 9")

Akin.update_hp(-1)
assert Akin.hp == 8, print("HP do Akin tinha que ser 8")

Akane.update_hp(-2)
assert Akane.hp == 2, print("HP do Akane tinha que ser 2")

Akane.reset_hp()
assert Akane.hp == 4, print("HP do Akane tinha que ser 4")

print("No errors in HP calculation! :)\n ----------------------------\n\n\n")