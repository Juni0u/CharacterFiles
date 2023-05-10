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
    def __init__(self,bin_rep=4, mut_prob=0.05):
        """binrep = how many bits represents each atribute
        mut_atrib = how many atributes go through mutation each time
        mut_prob = Mutation probability (between 0 and 1)"""
        self.bin_rep = bin_rep
        self.mut_prob = mut_prob

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
#        print("Pdr"+binPdr+",Pre"+binPre+",Defe"+binDefe+",Con"+binCon)
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
    
    def crossover (self,gene1,gene2):
        """[atrib1][atrib2][atrib3][atrib4]
        each time one of the three beginning positions will be chosen (beginning of atrib1, 2 or 3)
        and also a final position too, after the beginning one.
        One part will be from gene1 and the other from gene2"""
        #               10
        # 0123  4567  8901  2345
        #[0000][0000][0000][0000]
        gene1 = list(gene1)
        gene2 = list(gene2)
        gene_out1 = [None]*self.bin_rep*4
        gene_out2 = [None]*self.bin_rep*4
        start = [i*self.bin_rep for i in range(self.bin_rep)]              #possible positions to beginning positions of cut
        end = [i*self.bin_rep+self.bin_rep-1 for i in range(self.bin_rep)] #possible positions to ending positions of cut
        cut_in = rd.choice(start)
        cut_out = rd.choice(end)
        while (cut_out < cut_in):
            cut_out = rd.choice(end)
#        print("cutIN: ",cut_in,"// cutOUT: ",cut_out)  

        for i in range (cut_in,cut_out+1):
            gene_out1[i] = gene1[i]
            gene_out2[i] = gene2[i]
            
        for i in range(0,len(gene_out1)):
            if gene_out1[i] is None:
                gene_out1[i]=gene2[i]
            if gene_out2[i] is None:
                gene_out2[i]=gene1[i]

        gene_out1 = "".join(gene_out1)
        gene_out2 = "".join(gene_out2)     
        return gene_out1, gene_out2

    def mutation (self,gene):
        gene = list(gene)
        for i in range(0,len(gene)):
            prob = rd.random()
            if prob < self.mut_prob:
                if gene[i] == "0":
                    gene[i] = "1"
                else:
                    gene[i] = "0"
        return "".join(gene)    
    

        
