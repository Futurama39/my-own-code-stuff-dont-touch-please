import random


def fast(parent,moves,board):
    #always moves furthest along piece
    if len(moves) == 1:
        move = moves[0]
    else:
        prilist = [] #priority list
        for candidate in moves:
            
            if candidate.piece.status == 'live':
                priority = (candidate.piece.position - candidate.piece.parent.home ) % 40
            elif candidate.piece.status == 'home':
                priority = -1
            else:
                priority = -2
            if prilist == []:
                prilist.append([candidate,priority])
                continue
            else:
                for i in range(len(prilist)):
                    if priority > prilist[i][1]:
                        prilist.insert(i,[candidate,priority])
                        continue
                    else:
                        if i == len(prilist): # we are last and at the end of the list
                            prilist.append(candidate)
                            continue
        move = prilist[0][0] #pick best availible move
                        
    return move.piece


def rand(parent,moves,board):
    #picks moves randomly
    return random.choice(moves).piece
def rand_no_safe(parent,moves,board):
    yesmoves = []
    nomoves = []
    for move in moves:
        if move.piece.status != 'safe':
            yesmoves.append(move)
        else:
            nomoves.append(move)
    if yesmoves != []:
        return random.choice(yesmoves)
    else:
        return random.choice(nomoves)

def fast_with_capture(parent,moves,board):
    #always moves furthest along piece
    #however always captures
    if len(moves) == 1:
        move = moves[0]
    else:
        prilist = [] #priority list
        for candidate in moves:
            
            if candidate.piece.status == 'live':
                priority = (candidate.piece.position - candidate.piece.parent.home ) % 40
            elif candidate.piece.status == 'home':
                priority = -1
            else:
                priority = -2
            if candidate.piece.captures:
                priority = 41
                #top priority for capturing moves
            if prilist == []:
                prilist.append([candidate,priority])
                continue
            else:
                for i in range(len(prilist)):
                    if priority > prilist[i][1]:
                        prilist.insert(i,[candidate,priority])
                        continue
                    else:
                        if i == len(prilist): # we are last and at the end of the list
                            prilist.append(candidate)
                            continue
        move = prilist[0][0] #pick best availible move
    return move.piece

def dangerzone(parent,moves,board):
    if len(moves) == 1:
        move = moves[0]
    else:
        #look for all live pieces on the board
        livepieces = []
        for square in board.board:
            if square != 0:
                livepieces.append(square)
        for piece in parent.pieces:
            if piece.status !- 'live':
                pass
            else:

        prilist = [] #priority list
        for candidate in moves:
            pass