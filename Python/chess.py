import torch.nn as nn
import torch.nn.functional as f 
import numpy as np


# pawn,knight,bishop,rook,queen,king - [1-6]

global bcheck, wcheck
bcheck = wcheck = False

def blankboard():
    row = np.array([4,2,3,6,5,3,2,4])
    board = np.zeros((8,8))
    board[1] = board[6] = np.ones((1,8))
    board[0] = board[7] = row
    return board

def Wmovelegal(board,pieceX,pieceY):
    var = board[pieceX,pieceY]
    out = []
    if var == 0 :
        return out
    elif var == 1:
        if board[pieceX+1,pieceY] == 0:
            out.append ([pieceX+1,pieceY])
        if pieceX == 1 and board[pieceX+2,pieceY] == 0:
            out.append ([pieceX+2, pieceY])
        if board[pieceX+1,pieceY+1] == 1:
            out.append ([pieceX+1,pieceY+1])
        if board[pieceX+1,pieceY-1] == 1:
            out.append ([pieceX+1,pieceY-1])
        

print(blankboard())
