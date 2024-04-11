import random as rd
from Character import Character

class GAtoolbox():
    """Toolbox used to integrate GA methods to the code"""
    
    def __init__(self, reference:Character, goal:float, battle_number:int=1000, pop_size:int=100, gen:int=300, elitism:float=5, mut_prob:float=3):
        """[ref] -> reference character
        [goal] -> % of wins desired for output character
        [battle_number] -> how many times reference character will battle each character of the population
        [pop_size] -> number of characters in the population 
        [gen] -> for how many generations the code will run
        [elitism] -> % of the characters from the population that will continue to the next generation
        [mut_prob] -> % chance of mutation probability"""
        self.ref = reference
        self.battle_number = battle_number
        self.goal = goal*battle_number/100 #number of desided wins out of battle_number
        self.pop_size = pop_size
        self.gen = gen
        self.elite = elitism
        self.mut_prob = mut_prob
        self.pop = self.generate_initial_population()

    def generate_initial_population(self):
        population = []
        for i in range(0,self.pop_size):
            pdr = self.ref.pdr + rd.randint(0,5)
            pre = self.ref.pre + rd.randint(0,5)
            defe = self.ref.defe + rd.randint(0,5)
            con = self.ref.con + rd.randint(0,5)
            population.append(Character(pdr,pre,defe,con))
        return population

    def evaluation(self, character:Character) -> float:
        """evaluates individual in respect to the quantity of [wins] and [rounds] it had in a tourney
        returns individual fitness
        fit is distance from goal. 0 is best."""
        rounds, wins = self.tourney(battle_number=self.battle_number, target=character)
        fit =  abs(self.goal - wins) #TODO: do a weighted sum to considerer rounds duration in evaluation too
        return fit

    def tourney (self, battle_number:int, target:Character) -> list[float,int]:
        """[reference] battles [target] [battle_number] times
        returns [average rounds number],[win number]
        used by evalution method"""
        wins = 0
        rounds = 0
        for _ in range(battle_number):
            battle_result, round_qty = self.ref.battle(target=target,drawWin=False, drawLimit=10)
            rounds += round_qty
            if not battle_result: #battle result is true only if caller wins. i want the wins of target!
                wins += 1
        rounds = rounds/battle_number
        return rounds, wins
    
    def crossover (self,char1:Character, char2:Character) -> tuple[Character, Character]: 
        """produces 2 children from [char1] and [char2]"""
        gene1 = char1.gene 
        gene2 = char2.gene 

        child1_gene = []
        child2_gene = []
        cut_point = 1 #half

        for i in range(0,4):
            if i <= cut_point:
                child1_gene.append(gene1[i]) 
                child2_gene.append(gene2[i]) 
            else:
                child1_gene.append(gene2[i]) 
                child2_gene.append(gene1[i]) 

        child1 = Character(pdr=child1_gene[0], pre=child1_gene[1], defe=child1_gene[2], con=child1_gene[3])
        child2 = Character(pdr=child2_gene[0], pre=child2_gene[1], defe=child2_gene[2], con=child2_gene[3])
        return child1, child2   

    def mutation (self,character:Character) -> Character:
        """every atribute has a chance to mutate
        returns character (mutated if managed to pass in probability check)"""
        char_gene = character.gene
        for i in range(0,4):
            if rd.random() <= self.mut_prob:
                mutation_value = rd.randint(-5,5)
                while mutation_value==0:
                    mutation_value = rd.randint(-5,5)
                char_gene[i] += mutation_value
        character.set_atributes(atribute_list=char_gene)
        return character
    
    def evolve(self):
        pass
            
    

        
