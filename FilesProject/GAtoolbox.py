import random as rd

class GAtoolbox():
    """Toolbox used to integrate GA methods to the code"""
    
    def __init__(self,bin_rep=5, mut_prob=0.03):
        """binrep = how many bits represents each atribute
        mut_atrib = how many atributes go through mutation each time
        mut_prob = Mutation probability (between 0 and 1)"""
#        self.parameters = parameter(PARAM_FILE) #TODO: Adjust a parameter file
        self.bin_rep = bin_rep
        self.mut_prob = mut_prob

        if mut_prob > 1 or mut_prob < 0:
            print("mut_prob out of bounds, value set to 0.03.")
            self.mut_prob = 0.03

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
            #print(i)
            output.append(int(bin[i:i+self.bin_rep],2))
        return output
    
    def crossover (self,gene1,gene2):
        """[atrib1][atrib2][atrib3][atrib4]
        each time one of the three beginning positions will be chosen (beginning of atrib1, 2 or 3)
        and also a final position too, after the beginning one.
        One part will be from gene1 and the other from gene2"""
        #               10
        # 01234  56789  01234  56789
        #[00000][00000][00000][00000]
        gene1 = list(gene1)
        gene2 = list(gene2)
        gene_out1 = [None]*self.bin_rep*4
        gene_out2 = [None]*self.bin_rep*4
        start = [i*self.bin_rep for i in range(4)]              #possible positions to beginning positions of cut
        #print(start)
        end = [i*self.bin_rep+self.bin_rep-1 for i in range(4)] #possible positions to ending positions of cut
        #print(end)
        cut_in = rd.choice(start)
        cut_out = rd.choice(end)
        while (cut_out < cut_in):
            cut_out = rd.choice(end)
        #print("cutIN: ",cut_in,"// cutOUT: ",cut_out)  

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
        #print("in: ", gene)
        gene = list(gene)
        for i in range(0,len(gene)-1):
            prob = rd.random()
            if prob < self.mut_prob:
                if gene[i] == "0":
                    gene[i] = "1"
                else:
                    gene[i] = "0"
        #print("out ", "".join(gene))
        #print()
        return "".join(gene)    
    

        
