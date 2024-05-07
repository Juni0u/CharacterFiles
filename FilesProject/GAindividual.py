from Character import Character
import uuid

class GAindividual(Character):

    def __init__(self, pdr: int, pre: int, defe: int, con: int, born_in: int):
        super().__init__(pdr, pre, defe, con)

        #GA stuff
        self.fit = 0 
        self.born_in=born_in #which generation was born

    def __str__(self) -> str:
        return (f"Fit = {self.fit}, Born in = {self.born_in}, Level {self.lvl} [{self.pdr},{self.pre},{self.defe},{self.con}], [{self.proportion[0]} | {self.proportion[1]} | {self.proportion[2]} | {self.proportion[3]}]")
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Character):        
            for i in range(0,len(self.gene)):
                if self.gene[i] != other.gene[i]:
                    return False
            return True
        return False
        """if isinstance(other, Character):
            return self.id == other.id
        return False"""
    
def demo():
    tyr = GAindividual(pdr=5,pre=5,defe=10,con=5)
    akin = GAindividual(5,10,5,5)
    print(akin.id)
    print(tyr.id)

if __name__ == "__main__":
    demo()