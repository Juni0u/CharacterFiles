import random as rd

class Game_system():

    def roll_dices(self):
    #TODO: Is there a critical role?    
        dice1 = rd.randint(1,6)  
        dice2 = rd.randint(1,6) 
        dice3 = rd.randint(1,6)
        return (dice1+dice2+dice3)

    def atk(self, target):
        """The attacker calls this function and gives its target as argument."""
        print(self.pre+self.lvlbonus+self.roll_dices())
        print(target.defense)
        
        if (self.pre+self.lvlbonus+self.roll_dices()) > target.defense:
            #TODO: Melhorar essa funcao. O que ela deve retornar? A qtd de Hp, um aviso se a luta acabou?
            target.update_hp(-self.pdr)
            if target.hp < 1:
                return [True, target] #Battle ended, attacker won
            else:
                return [False, target] #Batlle continues
    
    def update_hp (self, value):
        self.hp = self.hp + value

    def reset_hp (self):
        self.hp = self.con

class Character(Game_system):        
    def __init__(self,lvl, pdr,pre,defe,con):
        self.lvl = lvl
        self.pdr = pdr
        self.pre = pre 
        self.defe = defe
        self.con = con
        self.atrib_sum = self.pdr + self.pre + self.defe + self.con
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

    
