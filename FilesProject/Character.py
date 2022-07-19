import random as rd

class Character():
    def __new__(cls,lvl, pdr,pre,defe,con):
        if (pdr+pre+defe+con) != (lvl+6):
            return None
        else:
            instance = super().__new__(cls) 
            instance.lvl = lvl
            instance.pdr = pdr
            instance.pre = pre
            instance.defe = defe
            instance.con = con
            return instance
        
    def __init__(self,lvl, pdr,pre,defe,con):
        self.lvl = lvl
        self.pdr = pdr
        self.pre = pre 
        self.defe = defe
        self.con = con
        self.atrib_sum = self.pdr + self.pre + self.defe + self.con
        self.lvlbonus = int(self.lvl*3/4)
        self.hp = con
        
    def __str__(self):
        return ("Level: "+ str(self.lvl)+"\n"+
                "PODER: "+ str(self.pdr)+"\n"+
                "PRECISAO: "+ str(self.pre)+ "\n"+
                "DEFESA: "+ str(self.defe) +"\n"+
                "CONSTITUICAO: "+ str(self.con)+"\n")   
    
    def get_atk (self, dices):
        dice1 = dices[0]
        dice2 = dices[1]
        dice3 = dices[2]
        atk = self.pre + self.lvlbonus + dice1 + dice2 + dice3
        # print("atk is ",atk)
        return [atk, dice1, dice2, dice3]
    
    def get_def (self):
        # print("def is ", self.defe + self.lvlbonus + 10)
        return (self.defe + self.lvlbonus + 10) 
    
    def reset_hp (self):
        self.hp = self.con
    
    def update_hp (self, value):
        self.hp = self.hp + value