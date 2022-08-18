# -*- coding: utf-8 -*-
"""
@author: premjethwa, UTA ID : 1001861810
- About: The task in this programming assignment is to implement an agent that plays the Max-Connect4 game using search. 
- References: 
       1. Lecture material of Artificial Intelligence 1 by Prof. Vamsikrishna Gopiskrishna.
       2. Basic script structure written by Chris Conly.     
    
"""

import sys
import time
import math
import random
import itertools

#----------------Node structure for forming tree for Minimax algorithm using alpha-beta pruning------------------#
class node:
    def __init__(self, val = 0, child = []):
        self.val = val
        self.child = child
       
    #Function to create tree 
    def create_child(self, branch_factor, depth, pred):
        if depth == 0:
            return
        if depth == 2:
            for i in range(branch_factor):
                child1 = node(child = None)
                pred.child.append(child1)     
        for i in range(branch_factor):
            child1 = node(child = [])
            pred.child.append(child1)
            self.create_child(branch_factor, depth-1, child1)
        return child1
    
#--------------------------Maxconnect4 object to store gameboard and other related details-----------------------#
class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        random.seed()

    #Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    #Output current game status to console
    def printGameBoard(self):
        print ('------------------')
        for i in range(6):
            print (' |', end = "")
            for j in range(7):
                print(self.gameBoard[i][j], end = "")
            print ('| ')
        print ('------------------')
    
    def printGameBoard_dummy(self, board):
        print ('------------------')
        for i in range(6):
            print (' |', end = "")
            for j in range(7):
                print(board[i][j], end = "")
            print ('| ')
        print ('------------------')

    #Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    #Output current game status to file - custom function
    def printGameBoardToFile_custom(self, h):
        for row in self.gameBoard:
            self.gameFile[h].write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile[h].write('%s\r\n' % str(self.currentTurn))

    #Place the current player's piece in the requested column
    def playPiece(self, column):
        if self.gameBoard[0][column] == 0:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1
        return -1
                
    #Place the current player's piece in the requested column of dummy board provided
    def playPiece_dummy(self, column, board, currentTurn):
        if board[0][column] == 0:
            for i in range(5, -1, -1):
                if board[i][column] == 0:
                    board[i][column] = currentTurn
                    return board, 0
        return board, -1

    #The AI section
    def aiPlay(self, depth):
        print("Machine is playing...")
        # Call minimax algorithm function
        column = self.Minimax(depth)
        # Play piece return by minimax algorithm
        result = self.playPiece(column-1)
        if not result:
            self.aiPlay(depth)
        else:
            print('\n\nMove %d: Player %d, Column %d\n' % (self.pieceCount, self.currentTurn, column))
            if self.currentTurn == 1:
                self.currentTurn = 2
            elif self.currentTurn == 2:
                self.currentTurn = 1

    #Function to calculate the scores and add it to leaf nodes
    def get_leaf_val(self, state, branch_factor, depth):
        root = state
        if not root:
            return []
        stack = []
        stack.append(root)
        last = None
        max_flag = (depth) % 2
        print(f"For Depth = {depth}")
        print(f"Creating tree and finding scores of board states after {depth - 1} moves")  
        moves = []
        for i in range(1, branch_factor + 1):
            moves.append(i)
        #Create combinations of all next "depth" number of moves possible
        comb = []
        for i in range(depth-1):
            comb.append(moves)
        p_moves = []
        for t in itertools.product(*comb):
            p_moves.append(list(t))
        #Visit each leaf node and write values to leaf nodes
        moves_ct = 0
        node_ct = 0
        while stack:
            root = stack[-1]
            if not root.child or last and (last in root.child):
                if root.child == None:
                    gcopy = [row[:] for row in self.gameBoard]   
                    ct = (((self.currentTurn-1) + 1) % 2) + 1
                    for m in p_moves[moves_ct]:
                        ct = (((ct-1) + 1) % 2) + 1
                        gcopy, check_flag = self.playPiece_dummy(m-1, gcopy, ct) 
                        if check_flag == -1:
                            break
                    if check_flag == -1:
                        if max_flag == 0:
                            root.val = -math.inf
                        else:
                            root.val = math.inf
                        check_flag = 0
                    else:
                        root.val = self.eval_func(gcopy)     
                    moves_ct += 1
                node_ct += 1
                stack.pop()
                last = root
            else:
                for children in root.child[::-1]:
                    stack.append(children)
        print("Completed forming tree")
        print(f"Nodes formed: {node_ct}\nScores calculated for {moves_ct} nodes.")
        return state
    
    #----------------------------------------------Alpha-beta pruning function-----------------------------------#
    #Reference : Prof. Vamsikrishna Gopikrishna notes
    def AlphaBetaPruning(self, state):
        print("Starting alpha-beta pruning")
        state.val = self.MaxValue(state, -math.inf, math.inf)   #call to Max_value function
        #Following code determines the action to be returned depending upon the scores calculated using alpha-beta pruning
        col = []
        col_num = 0
        for i in state.child:
            if i.val != math.inf:
                col.append(i.val)
            else:
                col.append(0)
        gboard = self.gameBoard[0]
        valid = 0
        count = 0
        while valid == 0:
            col_num = col.index(max(col)) + 1
            if gboard[col_num-1] == 0:
                valid = 1
            else:
                col[col_num-1] = -math.inf
            count += 1
            if count == 9:
                break
        if count == 9:
            print("No moves available.")
            return -1
        else:
            print("Column selected by Minimax algorithm (alpha-beta pruning):", col_num)
        return col_num
        
    #Function to maximize the score
    #Reference : Prof. Vamsikrishna Gopikrishna notes
    def MaxValue(self, state, alpha, beta):
        if state.child == None:
            return state.val
        state.val = -math.inf
        for a, s in enumerate(state.child):
            state.val = max(state.val, self.MinValue(s, alpha, beta))
            if state.val >= beta:
                return state.val
            alpha = max(alpha,state.val)
        return state.val
    
    #Function to minimize the score
    #Reference : Prof. Vamsikrishna Gopikrishna notes
    def MinValue(self, state, alpha, beta):
        if state.child == None:
            return state.val
        state.val = math.inf
        for a, s in enumerate(state.child):
            state.val = min(state.val, self.MaxValue(s, alpha, beta))
            if state.val <= alpha:
                return state.val
            beta = min(beta,state.val)
        return state.val
    
    #Function to perform Minimax algorithm by calling Alpha-Beta pruning function
    def Minimax(self, depth):
        if (42-self.pieceCount) <= 10:
            depth = 3
        branch_factor = 7
        create_child = node().create_child        
        root = node(child = [])
        create_child(branch_factor, depth, root)
        #Generate tree and calculate evaulation scores
        self.get_leaf_val(root, branch_factor, depth)
        #Call alpha beta pruning function
        column = self.AlphaBetaPruning(root)
        #return column selected by algorithm
        return column

    #Calculate the number of 4-in-a-row each player has on the game board passed
    def countScore_custom(self, board):
        player1Score = 0;
        player2Score = 0;
        #Check horizontally
        for row in board:
            #Check player A
            if row[0:4] == [1]*4:
                player1Score += 1
            if row[1:5] == [1]*4:
                player1Score += 1
            if row[2:6] == [1]*4:
                player1Score += 1
            if row[3:7] == [1]*4:
                player1Score += 1
            # Check player B
            if row[0:4] == [2]*4:
                player2Score += 1
            if row[1:5] == [2]*4:
                player2Score += 1
            if row[2:6] == [2]*4:
                player2Score += 1
            if row[3:7] == [2]*4:
                player2Score += 1

        #Check vertically
        for j in range(7):
            #Check player A
            if (board[0][j] == 1 and board[1][j] == 1 and
                   board[2][j] == 1 and board[3][j] == 1):
                player1Score += 1
            if (board[1][j] == 1 and board[2][j] == 1 and
                   board[3][j] == 1 and board[4][j] == 1):
                player1Score += 1
            if (board[2][j] == 1 and board[3][j] == 1 and
                   board[4][j] == 1 and board[5][j] == 1):
                player1Score += 1
            #Check player B
            if (board[0][j] == 2 and board[1][j] == 2 and
                   board[2][j] == 2 and board[3][j] == 2):
                player2Score += 1
            if (board[1][j] == 2 and board[2][j] == 2 and
                   board[3][j] == 2 and board[4][j] == 2):
                player2Score += 1
            if (board[2][j] == 2 and board[3][j] == 2 and
                   board[4][j] == 2 and board[5][j] == 2):
                player2Score += 1

        #Check diagonally
        #Check player A
        if (board[2][0] == 1 and board[3][1] == 1 and
               board[4][2] == 1 and board[5][3] == 1):
            player1Score += 1
        if (board[1][0] == 1 and board[2][1] == 1 and
               board[3][2] == 1 and board[4][3] == 1):
            player1Score += 1
        if (board[2][1] == 1 and board[3][2] == 1 and
               board[4][3] == 1 and board[5][4] == 1):
            player1Score += 1
        if (board[0][0] == 1 and board[1][1] == 1 and
               board[2][2] == 1 and board[3][3] == 1):
            player1Score += 1
        if (board[1][1] == 1 and board[2][2] == 1 and
               board[3][3] == 1 and board[4][4] == 1):
            player1Score += 1
        if (board[2][2] == 1 and board[3][3] == 1 and
               board[4][4] == 1 and board[5][5] == 1):
            player1Score += 1
        if (board[0][1] == 1 and board[1][2] == 1 and
               board[2][3] == 1 and board[3][4] == 1):
            player1Score += 1
        if (board[1][2] == 1 and board[2][3] == 1 and
               board[3][4] == 1 and board[4][5] == 1):
            player1Score += 1
        if (board[2][3] == 1 and board[3][4] == 1 and
               board[4][5] == 1 and board[5][6] == 1):
            player1Score += 1
        if (board[0][2] == 1 and board[1][3] == 1 and
               board[2][4] == 1 and board[3][5] == 1):
            player1Score += 1
        if (board[1][3] == 1 and board[2][4] == 1 and
               board[3][5] == 1 and board[4][6] == 1):
            player1Score += 1
        if (board[0][3] == 1 and board[1][4] == 1 and
               board[2][5] == 1 and board[3][6] == 1):
            player1Score += 1

        if (board[0][3] == 1 and board[1][2] == 1 and
               board[2][1] == 1 and board[3][0] == 1):
            player1Score += 1
        if (board[0][4] == 1 and board[1][3] == 1 and
               board[2][2] == 1 and board[3][1] == 1):
            player1Score += 1
        if (board[1][3] == 1 and board[2][2] == 1 and
               board[3][1] == 1 and board[4][0] == 1):
            player1Score += 1
        if (board[0][5] == 1 and board[1][4] == 1 and
               board[2][3] == 1 and board[3][2] == 1):
            player1Score += 1
        if (board[1][4] == 1 and board[2][3] == 1 and
               board[3][2] == 1 and board[4][1] == 1):
            player1Score += 1
        if (board[2][3] == 1 and board[3][2] == 1 and
               board[4][1] == 1 and board[5][0] == 1):
            player1Score += 1
        if (board[0][6] == 1 and board[1][5] == 1 and
               board[2][4] == 1 and board[3][3] == 1):
            player1Score += 1
        if (board[1][5] == 1 and board[2][4] == 1 and
               board[3][3] == 1 and board[4][2] == 1):
            player1Score += 1
        if (board[2][4] == 1 and board[3][3] == 1 and
               board[4][2] == 1 and board[5][1] == 1):
            player1Score += 1
        if (board[1][6] == 1 and board[2][5] == 1 and
               board[3][4] == 1 and board[4][3] == 1):
            player1Score += 1
        if (board[2][5] == 1 and board[3][4] == 1 and
               board[4][3] == 1 and board[5][2] == 1):
            player1Score += 1
        if (board[2][6] == 1 and board[3][5] == 1 and
               board[4][4] == 1 and board[5][3] == 1):
            player1Score += 1

        #Check player B
        if (board[2][0] == 2 and board[3][1] == 2 and
               board[4][2] == 2 and board[5][3] == 2):
            player2Score += 1
        if (board[1][0] == 2 and board[2][1] == 2 and
               board[3][2] == 2 and board[4][3] == 2):
            player2Score += 1
        if (board[2][1] == 2 and board[3][2] == 2 and
               board[4][3] == 2 and board[5][4] == 2):
            player2Score += 1
        if (board[0][0] == 2 and board[1][1] == 2 and
               board[2][2] == 2 and board[3][3] == 2):
            player2Score += 1
        if (board[1][1] == 2 and board[2][2] == 2 and
               board[3][3] == 2 and board[4][4] == 2):
            player2Score += 1
        if (board[2][2] == 2 and board[3][3] == 2 and
               board[4][4] == 2 and board[5][5] == 2):
            player2Score += 1
        if (board[0][1] == 2 and board[1][2] == 2 and
               board[2][3] == 2 and board[3][4] == 2):
            player2Score += 1
        if (board[1][2] == 2 and board[2][3] == 2 and
               board[3][4] == 2 and board[4][5] == 2):
            player2Score += 1
        if (board[2][3] == 2 and board[3][4] == 2 and
               board[4][5] == 2 and board[5][6] == 2):
            player2Score += 1
        if (board[0][2] == 2 and board[1][3] == 2 and
               board[2][4] == 2 and board[3][5] == 2):
            player2Score += 1
        if (board[1][3] == 2 and board[2][4] == 2 and
               board[3][5] == 2 and board[4][6] == 2):
            player2Score += 1
        if (board[0][3] == 2 and board[1][4] == 2 and
               board[2][5] == 2 and board[3][6] == 2):
            player2Score += 1

        if (board[0][3] == 2 and board[1][2] == 2 and
               board[2][1] == 2 and board[3][0] == 2):
            player2Score += 1
        if (board[0][4] == 2 and board[1][3] == 2 and
               board[2][2] == 2 and board[3][1] == 2):
            player2Score += 1
        if (board[1][3] == 2 and board[2][2] == 2 and
               board[3][1] == 2 and board[4][0] == 2):
            player2Score += 1
        if (board[0][5] == 2 and board[1][4] == 2 and
               board[2][3] == 2 and board[3][2] == 2):
            player2Score += 1
        if (board[1][4] == 2 and board[2][3] == 2 and
               board[3][2] == 2 and board[4][1] == 2):
            player2Score += 1
        if (board[2][3] == 2 and board[3][2] == 2 and
               board[4][1] == 2 and board[5][0] == 2):
            player2Score += 1
        if (board[0][6] == 2 and board[1][5] == 2 and
               board[2][4] == 2 and board[3][3] == 2):
            player2Score += 1
        if (board[1][5] == 2 and board[2][4] == 2 and
               board[3][3] == 2 and board[4][2] == 2):
            player2Score += 1
        if (board[2][4] == 2 and board[3][3] == 2 and
               board[4][2] == 2 and board[5][1] == 2):
            player2Score += 1
        if (board[1][6] == 2 and board[2][5] == 2 and
               board[3][4] == 2 and board[4][3] == 2):
            player2Score += 1
        if (board[2][5] == 2 and board[3][4] == 2 and
               board[4][3] == 2 and board[5][2] == 2):
            player2Score += 1
        if (board[2][6] == 2 and board[3][5] == 2 and
               board[4][4] == 2 and board[5][3] == 2):
            player2Score += 1
        
        return player1Score, player2Score
            
    #Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0;
        self.player2Score = 0
        #Check horizontally
        for row in self.gameBoard:
            #Check player A
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            #Check player B
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        #Check vertically
        for j in range(7):
            #Check player A
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            #Check player B
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        #Check diagonally
        #Check player A
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        #Check player B
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1

    #Function to apply masks to gameboard in order to evaluate evaluation scores
    def maskify(self, arr, mask):
        #Level weights: more weight value to lower rows compared to higher rows
        h = [[1,1,1,1,1,1,1],[2,2,2,2,2,2,2],[3,3,3,3,3,3,3],[4,4,4,4,4,4,4],[5,5,5,5,5,5,5],[6,6,6,6,6,6,6]]
        arr1 = [row[:] for row in arr]
        if len(arr) != len(mask) or len(arr[1]) != len(mask[1]):
            print("Error: Size of array is passed but mask is not same.")
            return []
        for i in range(len(arr1)):
            for j in range(len(arr1[1])):
                if mask[i][j] == "$":
                    arr[i][j] = -abs(arr[i][j]) ** h[i][j]
                elif mask[i][j] == "#":
                    arr[i][j] = abs(arr[i][j]) ** h[i][j]
                else:
                    arr1[i][j] = (arr[i][j] * mask[i][j]) ** (h[i][j])
        return sum(sum(arr1,[]))
    
    #Function to generate masks 
    def MaskGenerator(self):
        mask = []
        #Horizontal check
        mask.append([[1,1,1,1,0,0,0],["#","#","#","#",0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([["$","$","$","$",0,0,0],[1,1,1,1,0,0,0],["#","#","#","#",0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],["$","$","$","$",0,0,0],[1,1,1,1,0,0,0],["#","#","#","#",0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],["$","$","$","$",0,0,0],[1,1,1,1,0,0,0],["#","#","#","#",0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],["$","$","$","$",0,0,0],[1,1,1,1,0,0,0],["#","#","#","#",0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],["$","$","$","$",0,0,0],[1,1,1,1,0,0,0]])
        mask.append([[0,1,1,1,1,0,0],[0,"#","#","#","#",0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,"$","$","$","$",0,0],[0,1,1,1,1,0,0],[0,"#","#","#","#",0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,"$","$","$","$",0,0],[0,1,1,1,1,0,0],[0,"#","#","#","#",0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,"$","$","$","$",0,0],[0,1,1,1,1,0,0],[0,"#","#","#","#",0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,"$","$","$","$",0,0],[0,1,1,1,1,0,0],[0,"#","#","#","#",0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,"$","$","$","$",0,0],[0,1,1,1,1,0,0]])
        mask.append([[0,0,1,1,1,1,0],[0,0,"#","#","#","#",0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,"$","$","$","$",0],[0,0,1,1,1,1,0],[0,0,"#","#","#","#",0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,"$","$","$","$",0],[0,0,1,1,1,1,0],[0,0,"#","#","#","#",0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,"$","$","$","$",0],[0,0,1,1,1,1,0],[0,0,"#","#","#","#",0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,"$","$","$","$",0],[0,0,1,1,1,1,0],[0,0,"#","#","#","#",0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,"$","$","$","$",0],[0,0,1,1,1,1,0]])
        mask.append([[0,0,0,1,1,1,1],[0,0,0,"#","#","#","#"],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,"$","$","$","$"],[0,0,0,1,1,1,1],[0,0,0,"#","#","#","#"],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,"$","$","$","$"],[0,0,0,1,1,1,1],[0,0,0,"#","#","#","#"],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,"$","$","$","$"],[0,0,0,1,1,1,1],[0,0,0,"#","#","#","#"],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,"$","$","$","$"],[0,0,0,1,1,1,1],[0,0,0,"#","#","#","#"]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,"$","$","$","$"],[0,0,0,1,1,1,1]])
        #vertical check
        mask.append([[1,0,0,0,0,0,0],[1,0,0,0,0,0,0],[1,0,0,0,0,0,0],[1,0,0,0,0,0,0],["#",0,0,0,0,0,0],["#",0,0,0,0,0,0]])
        mask.append([["$",0,0,0,0,0,0],[1,0,0,0,0,0,0],[1,0,0,0,0,0,0],[1,0,0,0,0,0,0],[1,0,0,0,0,0,0],["#",0,0,0,0,0,0]])
        mask.append([["$",0,0,0,0,0,0],["$",0,0,0,0,0,0],[1,0,0,0,0,0,0],[1,0,0,0,0,0,0],[1,0,0,0,0,0,0],[1,0,0,0,0,0,0]])
        mask.append([[0,1,0,0,0,0,0],[0,1,0,0,0,0,0],[0,1,0,0,0,0,0],[0,1,0,0,0,0,0],[0,"#",0,0,0,0,0],[0,"#",0,0,0,0,0]])
        mask.append([[0,"$",0,0,0,0,0],[0,1,0,0,0,0,0],[0,1,0,0,0,0,0],[0,1,0,0,0,0,0],[0,1,0,0,0,0,0],[0,"#",0,0,0,0,0]])
        mask.append([[0,"$",0,0,0,0,0],[0,"$",0,0,0,0,0],[0,1,0,0,0,0,0],[0,1,0,0,0,0,0],[0,1,0,0,0,0,0],[0,1,0,0,0,0,0]])
        mask.append([[0,0,1,0,0,0,0],[0,0,1,0,0,0,0],[0,0,1,0,0,0,0],[0,0,1,0,0,0,0],[0,0,"#",0,0,0,0],[0,0,"#",0,0,0,0]])
        mask.append([[0,0,"$",0,0,0,0],[0,0,1,0,0,0,0],[0,0,1,0,0,0,0],[0,0,1,0,0,0,0],[0,0,1,0,0,0,0],[0,0,"#",0,0,0,0]])
        mask.append([[0,0,"$",0,0,0,0],[0,0,"$",0,0,0,0],[0,0,1,0,0,0,0],[0,0,1,0,0,0,0],[0,0,1,0,0,0,0],[0,0,1,0,0,0,0]])
        mask.append([[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,"#",0,0,0],[0,0,0,"#",0,0,0]])
        mask.append([[0,0,0,"$",0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,"#",0,0,0]])
        mask.append([[0,0,0,"$",0,0,0],[0,0,0,"$",0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0]])
        mask.append([[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,"#",0,0],[0,0,0,0,"#",0,0]])
        mask.append([[0,0,0,0,"$",0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,"#",0,0]])
        mask.append([[0,0,0,0,"$",0,0],[0,0,0,0,"$",0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0],[0,0,0,0,1,0,0]])
        mask.append([[0,0,0,0,0,1,0],[0,0,0,0,0,1,0],[0,0,0,0,0,1,0],[0,0,0,0,0,1,0],[0,0,0,0,0,"#",0],[0,0,0,0,0,"#",0]])
        mask.append([[0,0,0,0,0,"$",0],[0,0,0,0,0,1,0],[0,0,0,0,0,1,0],[0,0,0,0,0,1,0],[0,0,0,0,0,1,0],[0,0,0,0,0,"#",0]])
        mask.append([[0,0,0,0,0,"$",0],[0,0,0,0,0,"$",0],[0,0,0,0,0,1,0],[0,0,0,0,0,1,0],[0,0,0,0,0,1,0],[0,0,0,0,0,1,0]])
        mask.append([[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,"#"],[0,0,0,0,0,0,"#"]])
        mask.append([[0,0,0,0,0,0,"$"],[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,"#"]])
        mask.append([[0,0,0,0,0,0,"$"],[0,0,0,0,0,0,"$"],[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,1]])
        #Diogonal from top left to bottom right
        mask.append([[1,"$","$","$",0,0,0],["#",1,"$","$",0,0,0],["#","#",1,"$",0,0,0],["#","#","#",1,0,0,0],["#","#","#","#",0,0,0],[0,0,0,0,0,0,0]])
        mask.append([["$","$","$","$",0,0,0],[1,"$","$","$",0,0,0],["#",1,"$","$",0,0,0],["#","#",1,"$",0,0,0],["#","#","#",1,0,0,0],["#","#","#","#",0,0,0]])
        mask.append([[0,0,0,0,0,0,0],["$","$","$","$",0,0,0],[1,"$","$","$",0,0,0],["#",1,"$","$",0,0,0],["#","#",1,"$",0,0,0],["#","#","#",1,0,0,0]])
        mask.append([[0,1,"$","$","$",0,0],[0,"#",1,"$","$",0,0],[0,"#","#",1,"$",0,0],[0,"#","#","#",1,0,0],[0,"#","#","#","#",0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,"$","$","$","$",0,0],[0,1,"$","$","$",0,0],[0,"#",1,"$","$",0,0],[0,"#","#",1,"$",0,0],[0,"#","#","#",1,0,0],[0,"#","#","#","#",0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,"$","$","$","$",0,0],[0,1,"$","$","$",0,0],[0,"#",1,"$","$",0,0],[0,"#","#",1,"$",0,0],[0,"#","#","#",1,0,0]])
        mask.append([[0,0,1,"$","$","$",0],[0,0,"#",1,"$","$",0],[0,0,"#","#",1,"$",0],[0,0,"#","#","#",1,0],[0,0,"#","#","#","#",0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,"$","$","$","$",0],[0,0,1,"$","$","$",0],[0,0,"#",1,"$","$",0],[0,0,"#","#",1,"$",0],[0,0,"#","#","#",1,0],[0,0,"#","#","#","#",0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,"$","$","$","$",0],[0,0,1,"$","$","$",0],[0,0,"#",1,"$","$",0],[0,0,"#","#",1,"$",0],[0,0,"#","#","#",1,0]])
        mask.append([[0,0,0,1,"$","$","$"],[0,0,0,"#",1,"$","$"],[0,0,0,"#","#",1,"$"],[0,0,0,"#","#","#",1],[0,0,0,"#","#","#","#"],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,"$","$","$","$"],[0,0,0,1,"$","$","$"],[0,0,0,"#",1,"$","$"],[0,0,0,"#","#",1,"$"],[0,0,0,"#","#","#",1],[0,0,0,"#","#","#","#"]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,"$","$","$","$"],[0,0,0,1,"$","$","$"],[0,0,0,"#",1,"$","$"],[0,0,0,"#","#",1,"$"],[0,0,0,"#","#","#",1]])
        #Diogonal from bottom left to top right
        mask.append([["$","$","$",1,0,0,0],["$","$",1,"#",0,0,0],["$",1,"#","#",0,0,0],[1,"#","#","#",0,0,0],["#","#","#","#",0,0,0],[0,0,0,0,0,0,0]])
        mask.append([["$","$","$","$",0,0,0],["$","$","$",1,0,0,0],["$","$",1,"#",0,0,0],["$",1,"#","#",0,0,0],[1,"#","#","#",0,0,0],["#","#","#","#",0,0,0]])
        mask.append([[0,0,0,0,0,0,0],["$","$","$","$",0,0,0],["$","$","$",1,0,0,0],["$","$",1,"#",0,0,0],["$",1,"#","#",0,0,0],[1,"#","#","#",0,0,0]])
        mask.append([[0,"$","$","$",1,0,0],[0,"$","$",1,"#",0,0],[0,"$",1,"#","#",0,0],[0,1,"#","#","#",0,0],[0,"#","#","#","#",0,0],[0,0,0,0,0,0,0]])
        mask.append([[0,"$","$","$","$",0,0],[0,"$","$","$",1,0,0],[0,"$","$",1,"#",0,0],[0,"$",1,"#","#",0,0],[0,1,"#","#","#",0,0],[0,"#","#","#","#",0,0]])
        mask.append([[0,0,0,0,0,0,0],[0,"$","$","$","$",0,0],[0,"$","$","$",1,0,0],[0,"$","$",1,"#",0,0],[0,"$",1,"#","#",0,0],[0,1,"#","#","#",0,0]])
        mask.append([[0,0,"$","$","$",1,0],[0,0,"$","$",1,"#",0],[0,0,"$",1,"#","#",0],[0,0,1,"#","#","#",0],[0,0,"#","#","#","#",0],[0,0,0,0,0,0,0]])
        mask.append([[0,0,"$","$","$","$",0],[0,0,"$","$","$",1,0],[0,0,"$","$",1,"#",0],[0,0,"$",1,"#","#",0],[0,0,1,"#","#","#",0],[0,0,"#","#","#","#",0]])
        mask.append([[0,0,0,0,0,0,0],[0,0,"$","$","$","$",0],[0,0,"$","$","$",1,0],[0,0,"$","$",1,"#",0],[0,0,"$",1,"#","#",0],[0,0,1,"#","#","#",0]])
        mask.append([[0,0,0,"$","$","$",1],[0,0,0,"$","$",1,"#"],[0,0,0,"$",1,"#","#"],[0,0,0,1,"#","#","#"],[0,0,0,"#","#","#","#"],[0,0,0,0,0,0,0]])
        mask.append([[0,0,0,"$","$","$","$"],[0,0,0,"$","$","$",1],[0,0,0,"$","$",1,"#"],[0,0,0,"$",1,"#","#"],[0,0,0,1,"#","#","#"],[0,0,0,"#","#","#","#"]])
        mask.append([[0,0,0,0,0,0,0],[0,0,0,"$","$","$","$"],[0,0,0,"$","$","$",1],[0,0,0,"$","$",1,"#"],[0,0,0,"$",1,"#","#"],[0,0,0,1,"#","#","#"]])
        return mask

    #Evaluation function - 2: Used in main evaluation function 
    #Returns score of player A - score of player B
    def eval_func_custom(self, board):
        ct1 = self.currentTurn
        board_copy = [row[:] for row in board] 
        eval = 0
        if ct1 == 1:
            score1, score2 = self.countScore_custom(board_copy)
        else:
            score2, score1 = self.countScore_custom(board_copy)  
        eval = score1 - score2
        return eval

    #----------------------------------------------Main evaluation function--------------------------------------#
    def eval_func(self, board):
        mask_of = self.currentTurn
        board_copy1 = [row[:] for row in board] 
        board_copy2 = [row[:] for row in board] 
        for i in range(6):
            for j in range(7):
                if board_copy1[i][j] == mask_of:
                    board_copy1[i][j] = 1
                elif board_copy1[i][j] == 0:
                    board_copy1[i][j] = 0
                else:
                    board_copy1[i][j] = -1
        masks = self.MaskGenerator()
        eval = 0
        for mask in masks:
            val1 = self.maskify(board_copy1, mask)
            eval += (val1) + self.eval_func_custom(board_copy2)
        return eval
#-------------------------------------------End of maxConnect4Game class------------------------------------------#

#-------------------------Function to play one move and write back to output file------------------------------------
def oneMoveGame(currentGame, depth):
    if currentGame.pieceCount == 42:               
        print('BOARD FULL\n\nGame Over!\n')
        return

    currentGame.aiPlay(depth)
    print('Game state after move:')
    currentGame.printGameBoard()
    currentGame.countScore()
    print('Score: Player A = %d, Player B = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    currentGame.printGameBoardToFile()
    currentGame.gameFile.close()

#----------- ----Function to play interactive mode and write back to computer.txt and human.txt files------------#
def interactiveGame(currentGame, depth, cn_flag):
    player = input("Enter your player name: ")   
    if currentGame.pieceCount == 42:   
        print('BOARD FULL\n\nGame Over!\n')
        return
    ret = -1
    col = 1
    if cn_flag == 1:
        while currentGame.pieceCount != 42:
            print("\nPlayer: AI (Machine)")
            currentGame.aiPlay(depth) 
            print('Game state after move:')
            currentGame.printGameBoard()
            currentGame.printGameBoardToFile_custom(0)
            currentGame.countScore()
            print('Score: Player A = %d, Player B = %d\n' % (currentGame.player1Score, currentGame.player2Score))
            ret = -1
            print("\nPlayer:", player)
            print('Your turn. Select the column in which you want to enter piece.')
            while ret == -1:
                col = int(input("Enter value from 1 to 7 (-1 to stop game): "))
                if col == -1:
                    break
                col -= 1
                ret = currentGame.playPiece(col)
                if ret == -1:
                    print("Invalid column number. Please enter a value from 1 to 7.")
            if col == -1:
                print("Game terminated by", player)
                break
            if currentGame.currentTurn == 1:
                currentGame.currentTurn = 2
            elif currentGame.currentTurn == 2:
                currentGame.currentTurn = 1
            print('Game state after your move:')
            currentGame.printGameBoard()
            currentGame.printGameBoardToFile_custom(1)
            currentGame.countScore()
            print('Score: Player A = %d, Player B = %d\n' % (currentGame.player1Score, currentGame.player2Score))
    else: #else human plays first
        while currentGame.pieceCount != 42:
            ret = -1
            print("\nPlayer:", player)
            print('Your turn. Select the column in which you want to enter piece.')
            while ret == -1:
                col = int(input("Enter value from 1 to 7 (-1 to stop game): "))
                if col == -1:
                    break
                col -= 1
                ret = currentGame.playPiece(col)
                if ret == -1:
                    print("Invalid column number. Please enter a value from 1 to 7.")
            if col == -1:
                print("Game terminated by", player)
                break
            if currentGame.currentTurn == 1:
                currentGame.currentTurn = 2
            elif currentGame.currentTurn == 2:
                currentGame.currentTurn = 1
            print('Game state after your move:')
            currentGame.printGameBoard()
            currentGame.printGameBoardToFile_custom(1)
            currentGame.countScore()
            print('Score: Player A = %d, Player B = %d\n' % (currentGame.player1Score, currentGame.player2Score))
            print("\nPlayer: AI (Machine)")
            currentGame.aiPlay(depth) 
            print('Game state after move:')
            currentGame.printGameBoard()
            currentGame.printGameBoardToFile_custom(0)
            currentGame.countScore()
            print('Score: Player A = %d, Player B = %d\n' % (currentGame.player1Score, currentGame.player2Score))
            
    currentGame.gameFile[0].close()
    currentGame.gameFile[1].close()
    
    #Print final score and display the winner
    print("Game Over!!")
    print('Final score: Player A = %d, Player B = %d' % (currentGame.player1Score, currentGame.player2Score))
    if currentGame.player1Score > currentGame.player2Score:
        print("Player A wins")
    elif currentGame.player1Score < currentGame.player2Score:
        print("Player B wins")
    else:
        print("Game ended with a draw.!!")
    
#----------------------------------------------------Main function-----------------------------------------------#
def main(argv):
    start = time.time()
    if len(argv) != 5:
        print('Four command-line argvuments are needed:')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        return
    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        return
    currentGame = maxConnect4Game() # Create a game
    
    #Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
        file_lines = currentGame.gameFile.readlines()
        currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
        currentGame.currentTurn = int(file_lines[-1][0])
        currentGame.gameFile.close()
    except Exception :
        print("\nError opening input file.\nStarting with a blank board\n")
        currentGame.gameBoard = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]    
    
    #Start game
    print('\nMax-Connect4 game\n')
    print('Initial Game state before move:')
    currentGame.printGameBoard()

    #Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player A = %d, Player B = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    try:
        depth = int(argv[4])
        if depth <= 1:
            print("Error: Depth value entered is less than 2")
            return
    except Exception :
        print("Error: Depth value entered is not integer value.")
        return
        
    #if game mode given as interactive then call interactiveGame function
    if game_mode == 'interactive':
        print("\nEntering Interactive mode:\n")
        comp_next = argv[3]
        if comp_next != 'computer-next' and comp_next != 'human-next':
            print("Error: computer-first/ human-first value is not valid.")
            print("Valid values are: 1. computer-next  2. human-next\n\nExiting code")
            return
        if comp_next == 'computer-next':
            cn_flag = 1
        else:
            cn_flag = 0
        currentGame.gameFile = []
        
        outFile = 'computer.txt'
        try:
            currentGame.gameFile.append(open(outFile, 'w'))
        except:
            print('Error opening output file.')
            return
        
        outFile = 'human.txt'
        try:
            currentGame.gameFile.append(open(outFile, 'w'))
        except Exception:
            print('Error opening output file.')
            return
        interactiveGame(currentGame, depth, cn_flag) 
    else: 
        print("\nEntering one-move mode:\n")
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except Exception:
            print('Error opening output file.')
            return
        oneMoveGame(currentGame, depth) 
    end = time.time()   
    #For one move mode, print the time required
    if game_mode == "one-move":
        print("Start time:", start)
        print("Finish time:", end)
        print("Execution Time =", (end - start), "seconds")

if __name__ == '__main__':
    main(sys.argv)
    
#---------------------------------------------------End of program-----------------------------------------------#