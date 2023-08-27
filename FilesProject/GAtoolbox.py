import random as rd
from GameSystem import GameSystem as gs
from GameSystem import Character as char
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

class parameter(object):
    def __init__(self, archive_name):
        with open(archive_name,'r') as arq:
            parameter = json.load(arq)

        self.COLOR_LIST = parameter["COLOR_LIST"]

class GAtoolbox():
    """Toolbox used to integrate GA methods to the code"""
    
    def __init__(self,wins_goal,duration_goal,battle_number,
                 pop_size, gen,
                 start_pop = [],
                 mut_prob=0.03, 
                 weight_wins=0, weight_duration=1
                 ):
        """
        wins_goal in how much % of wins,
        duration_goal in how many rounds the fights took in average,
        battle_number -> how many battles each individual will fight agaisnt the reference, the more more precise but itll take more time,
        pop_size -> population size
        gen -> how many generations to run
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
        self.mut_prob = mut_prob
        self.weight_wins = weight_wins
        self.weight_duration = weight_duration
        if mut_prob > 1 or mut_prob < 0:
            raise (MutationProbIsOutOfBounds)
        if (weight_duration+weight_wins) != 1:
            raise(WeightSumIsNotOne)

  
    def reproduction (self,char1,char2): #crossover

        parent1 = char1.get_atrib_list()
        parent2 = char2.get_atrib_list()

        n = rd.randint(1,3)
        print("n is ",n)
        begin_parent1 = rd.choice([True,False])
        print("begin parent1 is ", begin_parent1)

        if begin_parent1:
            child1 = parent1[:n] + parent2[n:]
            child2 = parent2[:n] + parent1[n:]
        else:
            child1 = parent2[:n] + parent1[n:]
            child2 = parent1[:n] + parent2[n:]

        child1.append(char2.lvl)
        child2.append(char1.lvl)

        child1 = char(child1[0], child1[1], child1[2], child1[3], child1[4],)
        child2 = char(child2[0], child2[1], child2[2], child2[3], child2[4],)
        return child1, child2

    def mutation (self,char1):
        operation = [5,4,3,2,1,-1,-2,-3,-4,-5]
        mutated_char = char1.get_atrib_list(lvl=True)

        for i,atrib in enumerate(mutated_char): 
            if (rd.random() < self.mut_prob):
                mutated_char[i] += rd.choice(operation)

        mutated_char = char(mutated_char[0], mutated_char[1], mutated_char[2], mutated_char[3], mutated_char[4])
        return mutated_char
    
    def create_population (self, lvl):
        """Creates the population of n individuals of level lvl"""
        players = []
        GA_pop = []
        for i in range (0,self.pop_size):
            pdr = rd.randint(0, lvl+1)
            pre = rd.randint(0, lvl+1-pdr) 
            defe = rd.randint(0, lvl+1-pdr-pre)
            con = (lvl+1-pdr-pre-defe)
            players.append(char(pdr+1,pre+1,defe+1,con+3,lvl))
            GA_pop.append(GAindividual(id=i+1,character_obj=players[i]))
        return GA_pop

    def fitness_function(self, wins, avg_dur):
        fit = (abs(wins - self.wins_goal) * self.weight_wins) + (abs(avg_dur - self.duration_goal) * self.weight_duration)
        return fit

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
            self.start_pop = self.create_population(ref.character.lvl)
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
    #comment
        
