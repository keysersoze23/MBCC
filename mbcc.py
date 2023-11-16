import pandas as pd
import numpy as np
import random


# Negative Odds: 1 - (100 / Odds) = Decimal Odds
# Positive Odds: 1 + (Odds /100) = Decimal Odds

# create more games, random picking of games, slight favorite, random favorites, 
# create findOpponent function, simplifies conditional statements below, makes code more readable
# figure out way to better model min_positive rows, min_positive index
# looking into bankroll management
# sequence games, ABB, not necessarily random in parrandos
# markov decision process
# binomial trees
# change amount wagered depending on odds
# winOrloss function

class mbcc:

    def __init__(self, df, balance, col):

        self.df = df
        self.balance = balance
        self.wins = 0
        self.losses = 0
        self.counter = 1
        self.prob = []
        self.balance_vals = []
        self.col = col
    
    def getBalance(self):
        return int(self.balance)
    
    def getWins(self):
        return int(self.wins)
    
    def getLosses(self):
        return int(self.losses)
    
    def getAvgProb(self):
        return sum(self.prob)/len(self.prob)
    
    def incrementCounter(self):
        if self.counter > 3:
        #if self.counter == 3:
            self.counter = 1
        else:
            self.counter += 1
        
        return int(self.counter)

    def findOpponent(self, group, rowIndex):
        if rowIndex % 2 == 1:
            opponent = group.loc[rowIndex - 1]
        else:
            opponent = group.loc[rowIndex + 1]

        return opponent

    def winOrloss(self, backer, opponent):
        if int(backer['Final']) > int(opponent['Final']):
            return 'win'
        else:
            return 'loss'

    def bestUnderdog(self, group):
        # bestUnderdog is the game where you choose the underdog with the lowest payout
        # the team that is backed is the team with the least positive 'ML' value
        
        positive_rows = group[group[self.col] > 0]
        
        # If there are any positive values, get the row with the smallest one
        if not positive_rows.empty:
            min_positive_index = positive_rows[self.col].idxmin()
            backer = group.loc[min_positive_index]
            opponent = self.findOpponent(group, min_positive_index)
            self.prob.append(100 / (int(backer[self.col] + 100)))
            if self.winOrloss(backer, opponent) == 'win':
                self.balance += (int(backer[self.col])/100)
                self.wins += 1

            else:
                self.balance -= 1
                self.losses += 1

            self.balance_vals.append(tuple((backer['Date'], self.balance)))

        return self

    def worstUnderdog(self, group):
        # worstUnderdog is the game where you choose the underdog with the highest payout
        # the team that is backed is the team with the most positive 'ML' value
       
        positive_rows = group[group[self.col] > 0]

        # If there are any positive values, get the row with the smallest one
        if not positive_rows.empty:
            max_positive_index = positive_rows[self.col].idxmax()
            backer = group.loc[max_positive_index]
            opponent = self.findOpponent(group, max_positive_index)
            self.prob.append(100 / (int(backer[self.col] + 100)))
            if self.winOrloss(backer, opponent) == 'win':
                self.balance += (int(backer[self.col])/100)
                self.wins += 1

            else:
                self.balance -= 1
                self.losses += 1
            
            self.balance_vals.append(tuple((backer['Date'], self.balance)))

        
        return self

    def bestFavorite(self, group):
        # bestFavorite is the game where you choose the favorite with the lowest payout
        # the team that is backed is the team with the most negative 'ML' value
    
        negative_rows = group[group[self.col] < 0]

        # If there are any positive values, get the row with the smallest one
        if not negative_rows.empty:
            max_negative_index = negative_rows[self.col].idxmin()
            backer = group.loc[max_negative_index]
            opponent = self.findOpponent(group, max_negative_index)
            self.prob.append((-1*(int(backer[self.col]))) / (-1*(int(backer[self.col])) + 100))
            if self.winOrloss(backer, opponent) == 'win':
                self.balance += (-1 * (100/int(backer[self.col])))
                self.wins += 1

            else:
                self.balance -= 1
                self.losses += 1
            
            self.balance_vals.append(tuple((backer['Date'], self.balance)))

        
        return self

    def worstFavorite(self, group):
        # worstFavorite is the game where you choose the favorite with the highest payout
        # the team that is backed is the team with the least negative 'ML' value
    
        negative_rows = group[group[self.col] < 0]

        # If there are any positive values, get the row with the smallest one
        if not negative_rows.empty:
            max_negative_index = negative_rows[self.col].idxmax()
            backer = group.loc[max_negative_index]
            opponent = self.findOpponent(group, max_negative_index)
            self.prob.append((-1*(int(backer[self.col]))) / (-1*(int(backer[self.col])) + 100))
            if self.winOrloss(backer, opponent) == 'win':
                self.balance += (-1 * (100/int(backer[self.col])))
                self.wins += 1

            else:
                self.balance -= 1
                self.losses += 1

            self.balance_vals.append(tuple((backer['Date'], self.balance)))

        return self
    
    def homeUnderdog(self, group):
        # homeUnderdog is a home team that is expected to lose
        hometeam_positive_rows = group[(group['VH'] == 'H') & (group[self.col] > 0)]
        #hometeam_rows = group[group['VH'] == 'H' & group[self.col] > 0]        

        if not hometeam_positive_rows.empty:
            # backer = hometeam_positive_rows.sample(n=1)
            # backer_index_value = backer.index.item()
            backer_index_value = hometeam_positive_rows[self.col].idxmin()
            backer = group.loc[backer_index_value]
            opponent = self.findOpponent(group, backer_index_value)
            self.prob.append(100 / (int(backer[self.col] + 100)))
            if self.winOrloss(backer, opponent) == 'win':
                self.balance += (int(backer[self.col])/100)
                self.wins += 1

            else:
                self.balance -= 1
                self.losses += 1

            self.balance_vals.append(tuple((backer['Date'], self.balance)))

        return self

    
    def randomGame(self, group):
        # randomGame is the game where you choose a random game from that day
        backer = group.sample(n=1)
        random_row_index_value = backer.index.item()
        opponent = self.findOpponent(group, random_row_index_value)

        if self.winOrloss(backer, opponent) == 'win':
            if int(backer[self.col]) > 0:
                self.prob.append(100 / (int(backer[self.col] + 100)))
                self.balance += (-1 * (100/int(backer[self.col])))
                self.wins += 1
            else:
                self.prob.append((-1*(int(backer[self.col]))) / (-1*(int(backer[self.col])) + 100))
                self.balance += (-1 * (100/int(backer[self.col])))
                self.wins += 1

        else:
            self.balance -= 1
            self.losses += 1
        
        self.balance_vals.append(tuple((backer['Date'], self.balance)))

        return self

    def gameB(self, game1, game2, group, modulo):
        # gameB is where there are two games that are played based on if the payout is divisible by a selected integer
        # game1 is the game that is played if the value is not divisible by the selected integer
        # game2 is the game that is played if the value is divisible by the selected integer 
        if int(self.balance) % modulo == 0:
            self = game2(group)
        else:
            self = game1(group)

        return self
    
    def parrando(self, gameA, game1, game2, group, modulo, game_type = None):
        if game_type == 'rand':
            AorB= random.randint(1, 2)
            if AorB == 1:
                self = gameA(group)
            else: 
                self = self.gameB(game1, game2, group, modulo)
        else:
            
            if self.counter == 1:
                self = gameA(group)

            else:
                self = self.gameB(game1, game2, group, modulo)
            
            self.counter = self.incrementCounter()
            # print(self.counter)
        
        return self



# def parrando(key, df, mod_val, payout, balance, wins, losses, game_type, counter=None):
#     if game_type == 'rand':
#         AorB= random.randint(1, 2)
#         if AorB == 1:
#             balance, wins, losses = gameA(key, df, balance, wins, losses)
#         else: 
#             balance, wins, losses = gameB(key, df, mod_val, payout, balance, wins, losses)
#     else:
#         if counter == 1:
#             balance, wins, losses = gameA(key, df, balance, wins, losses)
#         else:
#             balance, wins, losses = gameB(key, df, mod_val, payout, balance, wins, losses)


    
#     return balance, wins, losses



          