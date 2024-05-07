import random as rd
import datetime
import copy
from Character import Character
from GAindividual import GAindividual

class GAtoolbox():
    """Toolbox used to integrate GA methods to the code"""
    
    def __init__(self, reference:Character, goal:float, battle_number:int=1000, pop_size:int=100, gen:int=300, elitism:float=5, mut_prob:float=3):
        """[ref] -> reference character\\
        [goal] -> % of wins desired for output character\\
        [battle_number] -> how many times reference character will battle each character of the population\\
        [pop_size] -> number of characters in the population \\
        [gen] -> for how many generations the code will run\\
        [elitism] -> % of the characters from the population that will continue to the next generation\\
        [mut_prob] -> % chance of mutation probability"""
        self.ref = reference
        self.battle_number = battle_number
        self.goal = int(goal*battle_number/100) #number of desided wins out of battle_number
        self.pop_size = pop_size
        self.gen = gen
        self.elite_num = int(elitism*pop_size/100) #number of elites in a population
        if self.elite_num == 0: self.elite_num = 1
        self.mut_prob = mut_prob/100
        self.pop = self.generate_initial_population()
        self.best = []

    def __str__(self) -> str:
        parameters = (f"""
                      Reference: {self.ref}
                      Number of battles: {self.battle_number}
                      Goal: {self.goal} wins
                      Population size: {self.pop_size}
                      Number of generations: {self.gen}
                      Mutation probability: {self.mut_prob}
                      Number of best NPCs: {len(self.best)}""")
        return parameters


    def generate_initial_population(self) -> list[GAindividual]:
        population = []
        focus_min = int(self.ref.lvl/3)
        focus_max = int(self.ref.lvl)

        #PDR
        for i in range(0,int(self.pop_size/4)):
            pdr = rd.randint(focus_min,focus_max)
            pre = rd.randint(0,self.ref.lvl-pdr)
            defe = rd.randint(0,self.ref.lvl-pdr-pre)
            con = self.ref.lvl-pdr-pre-defe
            population.append(GAindividual(pdr,pre,defe,con,0))

        #PRE
        for i in range(0,int(self.pop_size/4)):
            pre = rd.randint(focus_min,focus_max)
            pdr = rd.randint(0,self.ref.lvl-pre)
            defe = rd.randint(0,self.ref.lvl-pdr-pre)
            con = self.ref.lvl-pdr-pre-defe
            population.append(GAindividual(pdr,pre,defe,con,0))

        #DEFE
        for i in range(0,int(self.pop_size/4)):
            defe = rd.randint(focus_min,focus_max)
            pdr = rd.randint(0,self.ref.lvl-defe)
            pre = rd.randint(0,self.ref.lvl-pdr-defe)
            con = self.ref.lvl-pdr-pre-defe
            population.append(GAindividual(pdr,pre,defe,con,0))    

        #CON    
        for i in range(0,int(self.pop_size/4)):
            con = rd.randint(focus_min,focus_max)
            pdr = rd.randint(0,self.ref.lvl-con)
            defe = rd.randint(0,self.ref.lvl-pdr-con)
            pre = self.ref.lvl-pdr-pre-defe
            population.append(GAindividual(pdr,pre,defe,con,0))

        return population

    def evaluation(self, character:GAindividual) -> float:
        """character: GAindividual object; individual to be evaluated.
        Returns: individual fitness
        fit is distance from goal. 0 is best."""
        rounds, wins = self.tourney(battle_number=self.battle_number, target=character)
        #print(f"indiv:{character} ; wins: {wins}")
        fit =  abs(self.goal - wins) + (character.lvl - self.ref.lvl)*1.5 #lower lvl is better
        if fit < 0: fit = 0
        return fit

    def tourney (self, battle_number:int, target:GAindividual) -> list[float,int]:
        """target: GAindividual object; individual to battle against reference
        battle_number: int; number of battles reference and [target] go through.
        Returns: [rounds, wins]
            [rounds]: float; average number of rounds all battles took
            [wins]: int; number of victories [target] had"""
        wins = 0
        rounds = 0
        for _ in range(battle_number):
            battle_result, round_qty = self.ref.battle(target=target,drawWin=False, drawLimit=10)
            rounds += round_qty
            if not battle_result: #battle result is true only if caller wins. i want the wins of target!
                wins += 1
        rounds = rounds/battle_number
        return rounds, wins
    
    def crossover (self,char1:GAindividual, char2:GAindividual, gen:int) -> tuple[GAindividual, GAindividual]: 
        """char1, char2: GAindividual object; individuals to go through crossover.
        gen: int; current generation.
        Returns: tuple; children of [char1] and [char2]  
        """
        gene1 = char1.gene.copy() 
        gene2 = char2.gene.copy()

        child1_gene = []
        child2_gene = []
        cut_point = rd.randint(1,3)

        for i in range(0,4):
            if i < cut_point:
                child1_gene.append(gene1[i]) 
                child2_gene.append(gene2[i]) 
            else:
                child1_gene.append(gene2[i]) 
                child2_gene.append(gene1[i]) 

        child1 = GAindividual(pdr=child1_gene[0], pre=child1_gene[1], defe=child1_gene[2], con=child1_gene[3], born_in=gen)
        child2 = GAindividual(pdr=child2_gene[0], pre=child2_gene[1], defe=child2_gene[2], con=child2_gene[3], born_in=gen)
        child = rd.choice([child1,child2])
        return child
    
    def mutation (self,character:GAindividual) -> GAindividual:
        """character: GAindividual object; Individual to be tested if they'll go through mutation.
        Returns: Gaindividual object; Mutated individual (if suceeded in mutation probability check)"""
        char_gene = character.gene.copy()
        for i in range(0,4):
            if rd.random() <= self.mut_prob:
                mutation_value = rd.randint(-10,10)
                while mutation_value==0:
                    mutation_value = rd.randint(-10,10)
                char_gene[i] += mutation_value
        return character
         
    def evolve(self):
        #while len(self.best)<10:
            for g in range(0,self.gen+1):
                print(f"Generation {g}")
                
                #evaluate current population
                for indiv in self.pop:
                    indiv.fix_min_atributes()
                    indiv.atrib_proportion()
                    indiv.fit = self.evaluation(character=indiv)
                    if (indiv.fit<=15) and (indiv not in self.best): 
                        self.best.append(copy.copy(indiv)) 

                #self.output_archive(gen=g)

                #selection
                self.pop = sorted(self.pop, key=lambda x: x.fit)
                while len(self.pop)>self.pop_size:
                    self.pop.remove(self.pop[-1]) 

                if (g==self.gen): break #(len(self.best)>9)or

                #crossover
                for i in range (int(self.pop_size/2)):
                    parent1 = rd.choice(self.pop)
                    parent2 = rd.choice(self.pop)
                    while parent2==parent1:
                        parent2 = rd.choice(self.pop)
                    child = self.crossover(char1=parent1, char2=parent2, gen=g)
                    if child not in self.pop:
                        self.pop.append(child)

                #mutation          
                for indiv in self.pop:
                    indiv = self.mutation(character=indiv)

            #output archive
            self.best = sorted(self.best, key=lambda x: x.fit)
            self.output_archive()

    def output_archive(self,gen=""):
        import datetime

        current_datetime = datetime.datetime.now()
        date_time_string = current_datetime.strftime(f"{gen}___%Y-%m-%d_%H-%M-%S")

        filename = f"experiment_{date_time_string}.txt"

        with open(filename, 'w') as file:
            file.write(f"GENERATION {gen}\n")

            file.write(str(self))
            file.write("\nBest characters\n\n")
            for character in self.best:
                file.write(str(character))
                file.write("\n")

            file.write("\nLast population\n\n")
            for character in self.pop:
                file.write(str(character))
                file.write("\n")

def demo():
    ref = GAindividual(8,22,1,3,0)    

    GA = GAtoolbox(reference=ref, goal=70, battle_number=1000,
                   pop_size=100,gen=100,
                   elitism=0,mut_prob=3)
    GA.evolve()

if __name__ == "__main__":
    demo()
        
