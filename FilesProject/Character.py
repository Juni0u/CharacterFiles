import random as rd
import uuid


class Character():        
    def __init__(self, pdr:int,pre:int,defe:int,con:int):
        """Rules for character creation:
        - Starting points: 1 (PDR), 1(PRE), 1(DEFE), 3(CON) [6points]
        - Each lvl grants 1 point. In lvl 1 -> 1 Point to distribute; [lvl points]
        - Bonus Point depeding on the Race. Here this bonus is considered by the
        distribution of lvl+1 points. The extra point is the bonus point. [1points]
        - So the max sum each character can have is lvl + 6 + 1 = lvl + 7"""
        self.id = uuid.uuid4()

        self.pdr = pdr
        self.pre = pre 
        self.defe = defe
        self.con = con
        self.fix_min_atributes()
        self.gene = [pdr,pre,defe,con]
        self.atrib_proportion()
        
        # lvl could be one of the directly changed variables, but i decided not to.
        # because changing the lvl would mean that or  we have too many atributes (if lvl went down) or had atributes left to put (if lvl went up)
        ## the first one is not allowed, the second one is strange. why would a player not distribute one atribute? theres nothing to gain by holding it.
        ## the lvl is an implicit part of the game as it is accounted in both atk and defense. so in this case, lvl act as a bonus based on the sum of the atributes
        self.hp = con

    def __str__(self) -> str:
        return (f"Level {self.lvl}, [{self.pdr},{self.pre},{self.defe},{self.con}], [{self.proportion[0]},{self.proportion[1]},{self.proportion[2]},{self.proportion[3]}]")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Character):
            return self.id == other.id
        return False
    
    def atrib_proportion(self) -> None:
        proportion = []
        total = sum(self.gene)
        for atribute in self.gene:
            proportion.append(round(atribute/total,2))
        self.proportion = proportion

    def fix_min_atributes(self) -> None:
        """Theres a minimum for each atribute. This fuction makes sure the character fits in this condition."""
        if self.pdr < 1: self.pdr = 1
        if self.pre < 1: self.pre = 1
        if self.defe < 1: self.defe =1
        if self.con < 3: self.con += (3 - self.con)
        self.update_lvl()

    def set_atributes (self, atribute_list:list[int]) -> None:
        self.pdr = atribute_list[0]
        self.pre = atribute_list[1]
        self.defe = atribute_list[2]
        self.con = atribute_list[3]
        self.gene = [self.pdr, self.pre, self.defe, self.con] 
        self.update_lvl()

    def attack(self, target:"Character") -> bool:
        """The attacker calls this function and gives its target as argument.
        It returns true if the attack was successfull, False if not."""
        dices = self.roll_dices()
        if (self.pre+self.lvlbonus+dices) > target.defense:
            return True
        else:
            return False
        
    def update_lvl (self) -> None:
        """Updates character lvl"""
        self.lvl = (self.pdr + self.pre + self.defe + self.con) - 7
        self.lvlbonus = int(self.lvl*3/4)
        self.defense = self.defe + self.lvlbonus + 10
    
    def update_hp (self, value:int) -> None:
        """This function updates the HP of a character."""
        self.hp = self.hp + value

    def reset_hp (self) -> None:
        """This functions resets the HP of a character to full."""
        self.hp = self.con

    def roll_dices(self) -> int:
        #TODO: Is there a critical role?    
            """This function rolls 3 1d6 and returns the sum of them."""
            dice1 = rd.randint(1,6)  
            dice2 = rd.randint(1,6) 
            dice3 = rd.randint(1,6)
            return (dice1+dice2+dice3)
    
    def battle(self,target:"Character",drawWin:bool=False,drawLimit:int=10) -> list[bool,int]:
        """battle between caller character and [target].
        the fuction caller always attacks first.
        if [drawWin] is [True], draws are wins for caller. if [False], are losses.
        [drawLimit] is number of turns without end to declare a draw        
        returns [True] for called win, [False] for target win
        and number of rounds
        """
        self.reset_hp()
        target.reset_hp()
        rounds=0

        while rounds <= drawLimit:
            if self.attack(target=target):
                target.update_hp(-self.pdr)
                if target.hp < 1:
                    return [True, rounds]
            if target.attack(target=self):
                self.update_hp(-target.pdr)
                if self.hp < 1:
                    return [False, rounds]
            rounds += 1
        if drawWin:
            return [True, rounds]
        else:
            return [False, rounds]       


def demo():
    tyr = Character(pdr=5,pre=5,defe=10,con=5)
    akin = Character(5,10,5,5)
    print(akin)

if __name__ == "__main__":
    demo()

