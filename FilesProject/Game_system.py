import random as rd

class AttrOutOfRangeError(Exception):
    pass

class Game_system():

    def roll_dices(self):
    #TODO: Is there a critical role?    
        """This function rolls 3 1d6 and returns the sum of them."""
        dice1 = rd.randint(1,6)  
        dice2 = rd.randint(1,6) 
        dice3 = rd.randint(1,6)
        return (dice1+dice2+dice3)

    def attack(self, target):
        """The attacker calls this function and gives its target as argument.
        It returns true if the attack was successfull, False if not."""
        dices = self.roll_dices()
        #print("ATK:",self.pre+self.lvlbonus+dices)
        #print("DEF:",target.defense)
        if (self.pre+self.lvlbonus+dices) > target.defense:
            return True
        else:
            return False
    
    def update_hp (self, value):
        """This function updates the HP of a character."""
        self.hp = self.hp + value

    def reset_hp (self):
        """This functions resets the HP of a character to full."""
        self.hp = self.con

class Character(Game_system):        
    def __init__(self,lvl, pdr,pre,defe,con):
        """Rules for character creation:
        - Starting points: 1 (PDR), 1(PRE), 1(DEFE), 3(CON)
        - Each lvl grants 1 point. In lvl 1 -> 1 Point to distribute;
        - Bonus Point depeding on the Race. Here this bonus is considered by the
        distribution of lvl+1 points. The extra point is the bonus point."""

        if (pdr) < 1 or (pre) < 1 or (defe) < 1:
            raise AttrOutOfRangeError("POWER, PRECISION or DEFENSE is smaller than 1")
        elif (con) < 3:
            raise AttrOutOfRangeError("CONSTITUION is smaller than 3")
        elif (pdr+pre+defe+con) > lvl+7:
            raise AttrOutOfRangeError("Max atributes must be lvl+7")

        self.lvl = lvl
        self.pdr = pdr
        self.pre = pre 
        self.defe = defe
        self.con = con
        self.lvlbonus = int(self.lvl*3/4)
        self.defense = self.defe + self.lvlbonus + 10
        self.hp = con

    def __str__(self):
        return ("Level: "+ str(self.lvl)+"\n"+
                "PODER: "+ str(self.pdr)+"\n"+
                "PRECISAO: "+ str(self.pre)+ "\n"+
                "DEFESA: "+ str(self.defe) +"\n"+
                "CONSTITUICAO: "+ str(self.con)+"\n \n"+
                "HP: "+ str(self.hp)+"\n"+
                "Nivel Defesa: "+str(self.defense)+"\n")   


