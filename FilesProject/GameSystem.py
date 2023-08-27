import random as rd

class GameSystem():
    def roll_dices(self):
        """This function rolls 3 1d6 and returns the sum of them."""
        dice1 = rd.randint(1,6)  
        dice2 = rd.randint(1,6) 
        dice3 = rd.randint(1,6)
        return (dice1+dice2+dice3)

    def attack(self, target):
        """The attacker calls this function and gives its target as argument.
        It returns true if the attack was successfull, False if not."""
        dices = self.roll_dices()
        if (self.offense+dices) >= target.defense:
            return True
        else:
            return False
    
    def update_hp (self, value):
        """This function updates the HP of a character."""
        self.hp = self.hp + value

    def reset_hp (self):
        """This functions resets the HP of a character to full."""
        self.hp = self.con

    def battle (self, enemy, round_limit=25):
        """This function executes the battle itself.\n 
        I = Enemy that will be fighting\n
        O = True for ENEMY WIN"""
        rounds = 0
        self.reset_hp()
        enemy.reset_hp()

        while rounds < round_limit+1:
            rounds += 1
            if self.attack(enemy):
                enemy.update_hp(-self.pdr)
                if enemy.hp < 1:
                    return False, rounds
            if enemy.attack(self):     
                self.update_hp(-enemy.pdr)
                if self.hp < 1:
                    return True, rounds
        return False, rounds #if rounds > rounds limit then NPC LOST!
    
    def tourney (self, battle_number, enemy):
        """INPUTS: Number of battles self will battle enemy
        OUTPUT: number of wins enemy got, avg number of rounds battle took"""
        wins = 0
        rounds_sum = 0
        for i in range(0,battle_number):
            battle_result, round_qty = self.battle(enemy)
            #print("battle ",i," - result = ",battle_result)
            rounds_sum += round_qty
            if battle_result:
                wins += 1
        return wins, (rounds_sum/battle_number)
    
class Character(GameSystem):        
    def __init__(self, pdr,pre,defe,con,lvl=0):
        """Rules for character creation:
        - Starting points: 1 (PDR), 1(PRE), 1(DEFE), 3(CON) [6 total]
        - Each lvl grants 1 point. In lvl 1 -> 1 Point to distribute; [lvl + 6 total]
        - Bonus Point depeding on the Race. Here this bonus is considered by the
        distribution of lvl+1 points. The extra point is the bonus point. [lvl + 7 total]
        - So the max sum each character can have is lvl + 6 + 1 = lvl + 7
        - If the given lvl is 0, the level is calculated based on the point distribution"""
        

        # if (pdr) < 1 or (pre) < 1 or (defe) < 1:
        #     raise AttrOutOfRangeError("POWER, PRECISION or DEFENSE is smaller than 1")
        # elif (con) < 3:
        #     raise AttrOutOfRangeError("CONSTITUION is smaller than 3")
        # elif (pdr+pre+defe+con) > lvl+7:
        #     raise AttrOutOfRangeError("Max atributes must be lvl+7")

        self.pdr = pdr
        self.pre = pre 
        self.defe = defe
        self.con = con   

        #PRESTAR ATENCAO PRO VALOR DO LVL NUNCA SER MENOR QUER ZERO
        if lvl==0:
            self.fix_min_distribution()
            self.lvl = (pdr+pre+defe+con)-7
        else:
            self.lvl = lvl
            self.max_sum = self.lvl + 7
            self.fix_distribution()

        if self.lvl < 1:
            print("To aqui")
            print(self.lvl)
            #raise LvlIsBellowOne     

        self.lvlbonus = int(self.lvl*3/4)
        self.defense = self.defe + self.lvlbonus + 10
        self.offense = self.pre + self.lvlbonus # + 3d6
        self.hp = con

#        print("antes: ", self.pdr+self.pre+self.defe+self.con)
#        print("tem que ter: ", self.max_sum)
#        print()
#        print("depois: ", self.pdr+self.pre+self.defe+self.con)
#        print()


    def __str__(self):
        return ("Level: "+ str(self.lvl)+"\n"+
                "PODER: "+ str(self.pdr)+"\n"+
                "PRECISAO: "+ str(self.pre)+ "\n"+
                "DEFESA: "+ str(self.defe) +"\n"+
                "CONSTITUICAO: "+ str(self.con)+"\n \n"+
                "HP: "+ str(self.hp)+"\n"+
                "AtributosSum: "+str(self.pdr+self.pre+self.defe+self.con)+"\n"+
                "Nivel Defesa: "+str(self.defense)+"\n")   
    
    def fix_min_distribution(self):
        "Adjust atribute value if they are bellow the minimum"
        while self.pdr < 1:
            self.pdr += 1
        while self.pre < 1:
            self.pre += 1
        while self.defe < 1:
            self.defe += 1
        while self.con < 3:
            self.con +=1 

    def fix_distribution(self):
        "When the character lvl is given, its atributte distribution have to follow the rules"
        self.fix_min_distribution()
        atrib_list = self.get_atrib_list()
        while sum(atrib_list) > self.max_sum:
            if (atrib_list.index(max(atrib_list)) == 3) and (atrib_list[atrib_list.index(max(atrib_list))] == 3): #If biggest atrib is CON [index3] and its value is 3 (3 is its MINIMAL value)
                while True:
                    att = rd.randint(0,2) 
                    if atrib_list[att] != 1:
                        atrib_list[att] -= 1
                        break
            else:    
                atrib_list[atrib_list.index(max(atrib_list))] -= 1
        while sum(atrib_list) < self.max_sum: #if there are less atributes distributed, put the missing ones in con
            atrib_list[-1] += 1
        
        self.pdr = atrib_list[0]
        self.pre = atrib_list[1]
        self.defe = atrib_list[2]
        self.con = atrib_list[3]

    def get_atrib_list(self, lvl=False):
        if (lvl): return [self.pdr, self.pre, self.defe, self.con, self.lvl]
        else: return [self.pdr, self.pre, self.defe, self.con]

        