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

class GAtoolbox():
    """Toolbox used to integrate GA methods to the code"""
    def __init__(self,bin_rep=5,mut_qtd_atrib=4, mut_prob=0.05):
        """binrep = how many bits represents each atribute
        mut_atrib = how many atributes go through mutation each time
        mut_prob = Mutation probability (between 0 and 1)"""
        self.bin_rep = bin_rep
        self.mut_qtd_atrib = mut_qtd_atrib
        self.mut_prob = mut_prob

        if mut_qtd_atrib > 4 or mut_qtd_atrib < 1:
            print("mut_qtd_atrib out of bounds, value set to 4.")
            self.mut_qtd_atrib = 4
        if mut_prob > 1 or mut_prob < 0:
            print("mut_prob out of bounds, value set to 0.05.")
            self.mut_prob = 0.05

    def dec2bin(self,n):
        """Input: A number in decimal
        Output: The same in [bin_rep] bit binary"""
        output = bin(n)[2:].zfill(self.bin_rep)
        return(output)
    
    def char2gene(self,char):
        """Input: Character (object)
        Output: Character's attributes coded into binary"""
        binPdr=self.dec2bin(char.pdr)
        binPre=self.dec2bin(char.pre)
        binDefe=self.dec2bin(char.defe)
        binCon=self.dec2bin(char.con) 
        print("Pdr"+binPdr+",Pre"+binPre+",Defe"+binDefe+",Con"+binCon)
        return binPdr+binPre+binDefe+binCon
    
    def gene2char(self,bin):
        """Input: Binary
        Output: List [PDR,PRE,DEFE,CON]"""
        output = []
#        print("bin:",bin)
        for i in range(0,len(bin),self.bin_rep):
#            print(i)
            output.append(int(bin[i:i+self.bin_rep],2))
        return output
    
    def mutation (self,gene):
        """
        -> Pick a random number to see if it is bellow the mutation probability
        -> If it is, mutation occurs
        -> Goes to a loop to decide which atributes will be mutated each time
            > 1 atribute -> Change a random bit without caring its position
            > 2 atributes -> Pick 2 random attributes and mutate 1 bit in each
            > 3 atributes -> Pick 3 random attributes and mutate 1 bit in each
            > 4 atributes -> Mutate 1 bit in each"""
        prob = rd.random()
 #      print(prob)
 #      prob = 0.04
        atrib_list = []
        mutated_bits = []

        if prob < self.mut_prob:
            gene = list(gene)
            if (self.mut_qtd_atrib != 1):
                """If mutation is to happen in only 2 or 3 atributes:
                -> Random number between 1 and 4 are pick up
                -> This value is multiplied by quantity of bits tat represent each atributes
                -> This way it is possible to get to the most signiticant digit"""
                for i in range(1,self.mut_qtd_atrib+1):
                    atrib = rd.randint(1,4)
                    while atrib in atrib_list:
                        atrib = rd.randint(1,4)
                    atrib_list.append(atrib)

                for index in atrib_list:
 #               print("numero o atributo",index)
 #               print("posicao do bit mais significativo",index*self.bin_rep-5)
 #               print("bit da posicao acima",gene[index*self.bin_rep-5])
                    bit = rd.randint(index*self.bin_rep-5,index*self.bin_rep) # Get a random bit from this atribute
                    mutated_bits.append(bit)     
            else:
                mutated_bits = [rd.randint(0,len(gene)-1)]
        
#            print("mutated bits positions:",mutated_bits)   
            for each_bit in mutated_bits: 
                print("error",each_bit) #TODO:
                """Pdr00001,Pre00101,Defe01100,Con00100
genes origin 00001001010110000100
origin converted [1, 5, 12, 4]
error 12
error 20
Traceback (most recent call last):
  File "/home/nonato/GitRepository/CharacterFiles/FilesProject/main.py", line 95, in <module>
    mutation = tb.mutation(genes)
  File "/home/nonato/GitRepository/CharacterFiles/FilesProject/Game_system.py", line 151, in mutation
    if gene[each_bit] == "0": 
IndexError: list index out of range"""
                if gene[each_bit] == "0": 
                    gene[each_bit] = "1"
                else: 
                    gene[each_bit] = "0"
            return "".join(gene)
        else:
            return (gene)
            
        
