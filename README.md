The main goal of this is to practice Evolutionary Algorithms using python.
In order to do this, diferent evolutionary approaches will be applied to a specific problem.
In this case, the problem to be solved is NPC FILE CREATIONS FOR A FORUM RPG.

In this RPG each character has atributes that are compared when they battle. It is difficult for
a Game Master to build a balanced file for an enemy. The idea of this code is to take the burden of the
GM, so they can focus on story alone. This code will receive the Player's data (level and atributes), and 
a chosen probability of how many time this enemy would win the player in a fight. The GM might want to create
an easy enemy, so they can give as input 30%. This means this enemy won the Player 30% of the times in X number of
fights. The code will output the atributes of such enemy.
#TODO: DEFINE HOW MANY IS X;

In this system there are for atributes: POWER, PRECISION, DEFENSE and CONSTITUION.
    - POWER -> Used to calculate damage
    - PRECISION -> Used in attack action to define if it connects
    - DEFENSE -> Used in defense action to define if it connects
    - CONSTITUTION -> Character's HP

To define if an attack conects, the following test is done:
    
    (ATTACKER PRECISION + ATTACKER LVL * 3/4 + 3d6) x (DEFENDER DEFENSE + DEFENDER LVL * 3/4 + 10)
    
    If the attacker values are higher (and only higher) than the defender's, then the attack connects and the damage
    calculation follows up.

Damage calculation is simple:

    SUBTRACT from the DEFENDER'S CONSTITUION THE ATTACKER'S POWER ATTRIBUTE VALUE 

    Ex:. If the attacker has 4 POWER and defender has 10 CONSTITUION, and the attack connects,
    the defender's HP after damage calculation will be 6. (10 - 4 = 6)

There are rules for character creation:
    - Starting points: 1 (PDR), 1(PRE), 1(DEFE), 3(CON)
    - Each lvl grants 1 point. In lvl 1 -> 1 Point to distribute;
    - Bonus Point depeding on the Race. Here this bonus is considered by the
        distribution of lvl+1 points. The extra point is the bonus point.

*** During a battle the reference player always attacks first.