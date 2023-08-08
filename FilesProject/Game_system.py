import random as rd
import json
PARAM_FILE = "PARAMETERS.json"

class AttrOutOfRangeError(Exception):
    pass

class LvlIsBellowOne(Exception):
    pass

class MutationProbIsOutOfBounds(Exception):
    pass

class WeightSumIsNotOne(Exception):
    pass

class NotStartPopulationSet(Exception):
    pass

class PopulationIsNotMultipleOf4(Exception):
    pass

class parameter(object):
    def __init__(self, archive_name):
        with open(archive_name,'r') as arq:
            parameter = json.load(arq)

        self.COLOR_LIST = parameter["COLOR_LIST"]

class Game_system():
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

class Character(Game_system):        
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
        self.fix_min_distribution
        atrib_list = [self.pdr,self.pre,self.defe,self.con]
        while sum(atrib_list) > self.max_sum:
            if (atrib_list.index(max(atrib_list)) == 3) and (atrib_list[atrib_list.index(max(atrib_list))] == 3): #If biggest atrib is CON [index3] and its value is 3 (3 is its MINIMAL value)
                while True:
                    att = rd.randint(0,2) 
                    if atrib_list[att] != 1:
                        atrib_list[att] -= 1
                        break
            else:    
                atrib_list[atrib_list.index(max(atrib_list))] -= 1
        while sum(atrib_list) < self.max_sum:
            atrib_list[atrib_list.index(min(atrib_list))] += 1
        
        self.pdr = atrib_list[0]
        self.pre = atrib_list[1]
        self.defe = atrib_list[2]
        self.con = atrib_list[3]

class GAtoolbox():
    """Toolbox used to integrate GA methods to the code"""
    
    def __init__(self,wins_goal,duration_goal,battle_number,
                 pop_size, gen,
                 start_pop = [],
                 bin_rep=5, mut_prob=0.03, 
                 weight_wins=0.75, weight_duration=0.25
                 ):
        """binrep = how many bits represents each atribute\n
        mut_prob = Mutation probability (between 0 and 1)
        weight_wins/weight_duration = Weight to apply in fitness function, sum has to be 1."""
#        self.parameters = parameter(PARAM_FILE) #TODO: Adjust a parameter file
        self.start_pop = start_pop
        self.final_pop = []
        self.battle_number = battle_number
        self.wins_goal = int(battle_number * wins_goal/100)
        self.pop_size = pop_size
        self.gen = gen
        self.duration_goal = duration_goal
        self.bin_rep = bin_rep
        self.mut_prob = mut_prob
        self.weight_wins = weight_wins
        self.weight_duration = weight_duration
        if pop_size % 4 !=0:
            raise(PopulationIsNotMultipleOf4)
        if mut_prob > 1 or mut_prob < 0:
            raise (MutationProbIsOutOfBounds)
        if (weight_duration+weight_wins) != 1:
            raise(WeightSumIsNotOne)

    def dec2bin(self,n: int):
        """I = A number in decimal\n
        O = The same in [bin_rep] bit binary"""
        output = bin(n)[2:].zfill(self.bin_rep)
        return(output)
    
    def char2gene(self,char: object):
        """I = Character (object)\n
        O = Character's attributes coded into binary"""
        binPdr=self.dec2bin(char.pdr)
        binPre=self.dec2bin(char.pre)
        binDefe=self.dec2bin(char.defe)
        binCon=self.dec2bin(char.con) 
#        print("Pdr"+binPdr+",Pre"+binPre+",Defe"+binDefe+",Con"+binCon)
        return binPdr+binPre+binDefe+binCon
    
    def gene2char(self,bin):
        """I = Binary\n
        O = List [PDR,PRE,DEFE,CON]"""
        output = []
#        print("bin:",bin)
        for i in range(0,len(bin),self.bin_rep):
            #print(i)
            output.append(int(bin[i:i+self.bin_rep],2))
        return output
    
    def crossover (self,gene1,gene2):
        """[atrib1][atrib2][atrib3][atrib4]\n
        Each time one of the three beginning positions will be chosen (beginning of atrib1, 2 or 3)\n
        and also a final position too, after the beginning one.\n
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
    
    def fitness_function(self, wins, avg_dur):
        fit = (abs(wins - self.wins_goal) * self.weight_wins) + (abs(avg_dur - self.duration_goal) * self.weight_duration)
        return fit
    
    def create_population (self, lvl):
        """Creates the population of n individuals of level lvl"""
        players = []
        GA_pop = []
        for i in range (0,self.pop_size):
            pdr = rd.randint(0, lvl+1)
            pre = rd.randint(0, lvl+1-pdr) 
            defe = rd.randint(0, lvl+1-pdr-pre)
            con = (lvl+1-pdr-pre-defe)
            players.append(Character(pdr+1,pre+1,defe+1,con+3,lvl))
            GA_pop.append(GAindividual(id=i+1,character_obj=players[i]))
            self.start_pop = GA_pop

    def reproduction(self,parent1,parent2):
        """Function to reproduce. Mutation is run here too.
        Input: [GAindividual]: 2 Parents
        Output: [Character]: 2 children"""
        #Parents are transformed to genes 
        parent1 = self.char2gene(parent1.character)
        parent2 = self.char2gene(parent2.character)
        #Crossover is done, output is still genes
        children = self.crossover(parent1, parent2)
        children_final = []
        for child in children:
            #print("before:",child)
            #Mutation is run
            child = self.mutation(child)
            #print("after: ",child)
            #Child is transformed back to character object
            child = self.gene2char(child)
            child = Character(pdr=child[0],pre=child[1],defe=child[2],con=child[3])
            children_final.append(child)
        return children_final

    def selection(self,gen, pop):
        """Groups of 4 indiv. are randomly formed.
        The best goes to next gen.
        The second and third are chosen to reproduction set.
        The forth is killed."""
        tournment_group_size = 4
        parents = []  
        new_pop = []
        t_group = []
        for i in range(int(self.pop_size/tournment_group_size)):
            #print("i = ", i)
            t_group = rd.sample(pop,tournment_group_size)
            for element in t_group:
                pop.remove(element)
                
            elite = min(t_group, key=lambda obj: obj.fit)
            print(elite.fit)
            t_group.remove(elite)
            dead = max(t_group, key=lambda obj: obj.fit)
            t_group.remove(dead)
            survivors = t_group
            new_pop.append(elite)
            if gen==self.gen-1:
                continue
            parents += survivors
            #No final do loop de cima, todos os elites ja estao na nova populacao
            #Com os dois pais, cria-se dois filhos
            children = self.reproduction(survivors[0],survivors[1])
            for child in children:
                childGA = GAindividual(id=self.pop_size+gen*i,character_obj=child,fitness=99999) 
                new_pop.append(childGA)

        #Completando a populacao: dois pais sao selecionados aleatoriamente de todos os pais possiveis
        #o primeiro filho e utilizado e o segundo descatardo
        #isso e feito ate completar a populacao
        if gen != self.gen-1:
            for j in range(self.pop_size-len(new_pop)):
                #print("j = ", j)
                couple = rd.sample(parents,2)
                for parent in couple:
                    parents.remove(parent)
                child,_ = self.reproduction(couple[0],couple[1])
                childGA = GAindividual(id=self.pop_size+gen*i,character_obj=child,fitness=99999) 
                new_pop.append(childGA)
                #print(len(new_pop))




                
#                pop_fitness.remove(pop_fitness[choice])   # Remove ELEMENT for next choices
#            print("grupo = ", t_group)
#            new_pop.append(t_group.index(max(t_group))) #Put the best fit in the new_pop
#            t_group.remove(min(t_group)) #Remove the smallest fit
#            t_group.remove(max(t_group)) #Remove the biggest fit to prepare for next line
#            parents.extend(t_group)      #Put the rest into the parents to reproduce
#            print("Elites = ", new_pop)
#            print("Parents = ", parents)
#            print()
            t_group = []

        return new_pop

    def evolve(self, reference_player, filename="characters.txt"):
        ref = GAindividual(0,reference_player)
        if self.start_pop == []:
            self.create_population(ref.character.lvl)

        pop = self.start_pop
        for gen in range(self.gen):
            print("======================")
            print("Gen ", gen+1)

            # Calculate each individual's fitness
            for individual in pop: 
                result, rounds = ref.character.tourney(battle_number=self.battle_number, enemy=individual.character)
                individual_fit = self.fitness_function(wins=result,avg_dur=rounds)
                individual.setFit(new_fit=individual_fit)

            # Perform selection
            new_pop = self.selection(gen=gen,pop=pop)
            print("FITNESS = ",new_pop[0].fit)
            print(new_pop[0].character)
            
            #update population
            pop = new_pop
            new_pop = []
            print(len(pop))
        return pop

class GAindividual(GAtoolbox):
    def __init__(self, id, character_obj, fitness=99999):
        self.id = id                     #object identifier
        self.character = character_obj
        self.fit = fitness

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return str("id: "+str(self.id)+" / fitness: "+str(self.fit))
    
    def __eq__(self, other):
        if isinstance(other, GAindividual):
            return self.id == other.id
        return False

    def setFit(self, new_fit):
        self.fit = new_fit

    def getFit(self):
        return self.fit
        
