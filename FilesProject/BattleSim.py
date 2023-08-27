from FilesProject.GAtoolbox import Character as char
import random as rd
import numpy as np

def create_characters (n_player,player_lvl):
    players = []
    for i in range (0,n_player):
        pdr = rd.randint(0, player_lvl)
        pre = rd.randint(0, player_lvl-pdr)
        defe = rd.randint(0, player_lvl-pdr-pre)
        con = (player_lvl-pdr-pre-defe)
        players.append(char(player_lvl,pdr+1,pre+1,defe+1,con+3))
    return players

def roll_dices():
        dice1 = rd.randint(1,6)  
        dice2 = rd.randint(1,6) 
        dice3 = rd.randint(1,6)
        # print("dices:", dice1,dice2,dice3)
        return [dice1, dice2, dice3]

def turno (atker,defer,dices):
    if atker.get_atk(dices)[0] >= defer.get_def():
        return 1 #returns 1, atker won the battle
    else:
        return 0 #return 0, battle continues
        


#%%
n_player = 1500
player_lvl = 30
players = create_characters(n_player, player_lvl)
xvx = 60 # times each build plays agaisnt each other
# Tyr = char(10, 2, 4, 2, 8)
# Akin = char(10, 2, 2, 4, 8)
# players = [Tyr, Akin]
b_results = []
        
for k in range(0,int(xvx/2)):
    for i in range (0,n_player):
        if k==0:
            b_results.append(list(range(0,int(n_player*xvx/2))))
        player1 = players[i]
        for j in range (0,n_player):
            player2 = players[j]
            
            #important vars
            winner = "none"        # can be: l (line player - 1) / c (column player - 2) / d (draw)
            end_battle = False
            first_turn = True
            next_turn = 0       # who atks next turn? 1 or 2 (line or column)
            turn_numbers = 0
            player1.reset_hp()
            player2.reset_hp()     
            
            if j==i:
                winner = "x"
                end_battle = True
                
            #print players battleing
            # print()
            # print("-------------------")      
            # print("FIGHT!")
            # print("-------------------")      
            # print(player1)
            # print()  
            # print(player2)
    
            #%% INSIDE THIS IS A FIGHT between player 1 X player 2
            while (end_battle == False):
                if turn_numbers > 20:
                    winner = "None"
                    break
                #first turn
                if first_turn:
                    first_turn = False
                    turn_numbers += 1
                    both_mistake = True    # only usefull in first turn, in case both mistake the attack
                    if turno(player1, player2, roll_dices()):
                        player2.update_hp(-player1.pdr)
                        both_mistake = False
                    if turno(player2, player1, roll_dices()):
                        player1.update_hp(-player2.pdr)
                        both_mistake = False
                    if player1.hp < 1 and player2.hp < 1:
                        winner = "d" #draw
                        end_battle = True
                    elif player1.hp < 1:
                        winner = "c"
                        end_battle = True
                    elif player2.hp < 1:
                        winner = "l"
                        end_battle = True                    
                    elif player1.hp == player2.hp or both_mistake:
                        first_turn = True
                    elif player1.hp < player2.hp:
                        next_turn = 1
                    elif player2.hp < player1.hp:
                        next_turn = 2
                #not first turn:        
                else:
                    if next_turn == 1:
                        next_turn = 2
                        turn_numbers += 1
                        if turno(player1, player2, roll_dices()):
                            player2.update_hp(-player1.pdr)
                            if player2.hp < 1:
                                winner = "l"
                                end_battle = True
                    elif next_turn == 2:
                        next_turn = 1
                        turn_numbers += 1
                        if turno(player2, player1, roll_dices()):
                            player1.update_hp(-player2.pdr)
                            if player1.hp < 1:
                                winner = "c"
                                end_battle = True           
                # print("-------------------")      
                # print(player1)
                # print()  
                # print(player2)                            
    #% battle update
            b_results[i][j+(k*n_player)] = winner
                
#%% Results Analysis
victories = []
draws = []
losses = []
for line in b_results:
    victories.append(line.count("l"))
    draws.append(line.count("d"))
    losses.append(line.count("c"))
vic_max = max(victories)
draws_max = max(draws)
losses_max = max(losses)

player_max_vic = victories.index(vic_max)
player_max_draws = draws.index(draws_max)
player_max_losses = losses.index(losses_max)

print("Player que mais venceu: "+str(vic_max)+" vitorias")
print(players[player_max_vic])
print("-------------------------")
print("Player que mais empatou: "+str(draws_max)+" empates")
print(players[player_max_draws])
print("-------------------------")                  
print("Player que mais perdeu: "+str(losses_max)+" derrotas")
print(players[player_max_losses])
print("-------------------------")                  
                
#%%
print(players[8])
            
            
                
        


#%%






    
    