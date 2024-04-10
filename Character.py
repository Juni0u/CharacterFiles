class Character():        
    def __init__(self, pdr:int,pre:int,defe:int,con:int):
        """Rules for character creation:
        - Starting points: 1 (PDR), 1(PRE), 1(DEFE), 3(CON) [6points]
        - Each lvl grants 1 point. In lvl 1 -> 1 Point to distribute; [lvl points]
        - Bonus Point depeding on the Race. Here this bonus is considered by the
        distribution of lvl+1 points. The extra point is the bonus point. [1points]
        - So the max sum each character can have is lvl + 6 + 1 = lvl + 7"""

        self.pdr = pdr
        self.pre = pre 
        self.defe = defe
        self.con = con
        self.lvl = self.get_lvl()
        self.lvlbonus = int(self.lvl*3/4)
        self.defense = self.defe + self.lvlbonus + 10
        self.hp = con
        self.fix_distribution()

    def __str__(self) -> str:
        return ("Level: "+ str(self.lvl)+"\n"+
                "PODER: "+ str(self.pdr)+"\n"+
                "PRECISAO: "+ str(self.pre)+ "\n"+
                "DEFESA: "+ str(self.defe) +"\n"+
                "CONSTITUICAO: "+ str(self.con)+"\n \n"+
                "HP: "+ str(self.hp)+"\n"+
                "Nivel Defesa: "+str(self.defense)+"\n")   
    
    def get_lvl(self) -> int:
        """Returns the lvl of a character based on the amount of atributes used"""
        lvl = (self.pdr + self.pre + self.defe + self.con) - 7
        return (self.pdr)

    def attack(self, target:Character) -> bool:
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

    def roll_dices(self) -> int:
        #TODO: Is there a critical role?    
            """This function rolls 3 1d6 and returns the sum of them."""
            dice1 = rd.randint(1,6)  
            dice2 = rd.randint(1,6) 
            dice3 = rd.randint(1,6)
            return (dice1+dice2+dice3)
    
if __name__ == "__main__":
    tyr = Character(pdr=5,pre=5,defe=10,con=5)
    print(tyr)