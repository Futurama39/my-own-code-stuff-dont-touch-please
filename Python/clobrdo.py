'''
HOUSE RULES : 
Three dice rolls whenever all pieces not live
On a six you can either place or run
Place gets your piece on the board and ends your turn
Run moves a piece and gets you another roll
A double run does not get you a third roll
Moving is done whenever possible
'''

import random
import clobrdo_methods
class Board:
    def __init__(self):
        self.board = [0] * board_size #Piece objects are placed inside the 0's when placed
        self.turn_number = 0
        self.winner = None #if selected, a Player object declared into it
        #vars for passing to methods
        self.player_count = player_count
        self.board_size = board_size
        self.players = Players

    '''
    Piece operations
    While they have some checks they are for assertions not move legality checks
    The Board class is supposed for definite actions, use functions in the Player class
    It is assumed that all board functions called are leagal moves
    '''
    def place_piece(self,player):
        if self.board[player.home] != 0:
            self.remove_piece(player.home)
            #remove foreign piece located at player's home
        for piece in player.pieces:
            if piece.status == 'home': #locate first piece that is at home and can be placed on the board
                target_piece = piece
                break
        if 'target_piece' not in locals():
            print("target_piece not defined, something has gone terribly wrong")
        target_piece.position = player.home
        target_piece.status = 'live'
        self.board[player.home] = target_piece
        player.home_pieces -= 1
        player.live_pieces += 1

    def remove_piece(self,origin:int):
        #expects the position on self.board of the to be removed piece
        #also expects the target board position to be a piece
        piece = self.board[origin]
        piece.status = 'home'
        piece.position = -1
        piece.parent.live_pieces -= 1
        piece.parent.home_pieces += 1
        self.board[origin] = 0
    
    def move_piece(self,piece,amt:int):
        destination = piece.position + amt # no loopthru here for player 0 safepiece check, the destination is rewritten on the else clause
        if piece.position < piece.parent.terminator and destination > piece.parent.terminator:
            safe_board_position = destination - (piece.parent.terminator + 1) #one more is removed to get from position after the terminator to compatible list index
            self.board[piece.position] = 0 #remove piece from live board
            piece.status = 'safe'
            piece.parent.live_pieces -= 1
            piece.parent.safe_pieces += 1
            piece.parent.safeboard[safe_board_position] = piece
            piece.position = safe_board_position #i honetly hope that positions are handled with piece.status awareness and can be used aware to context and that it don't break stuff
        else:
            destination = (piece.position + amt) % board_size
            #piece moves to a destination on the live board
            if self.board[destination] != 0:
                #destination is occupied
                self.remove_piece(destination)
            self.board[piece.position] = 0 #free up the position place
            piece.position = (piece.position + amt) % board_size #move the postion place 
            self.board[piece.position] = piece #place piece at destination
    def safe_move(self,player,piece,amt:int):
        #amt is expectes as the roll not the destination
        player.safeboard[piece.position] = 0 #empty up original safeboard space
        piece.position += amt
        player.safeboard[piece.position] = piece #occupy new position

    def is_won(self,Players:list):
        #accepts the Players list
        for player in Players:
            if player.safe_pieces == piece_num:
                self.winner = player

class Player:
    def create_pieces(self,amt:int) -> list:
        out = [] #returns a list of Piece objects
        for _ in range(amt):
            out.append(Piece(self))
        return out

    def __init__(self,turnorder:int,ai_driver):
        self.wins = 0
        self.turn_order = turnorder
        self.home = 10 * self.turn_order #player 1 begins at 0 and then by increments of 10
        self.terminator = (self.home + board_size - 1) % board_size #last piece of the circle for player
        self.driver = ai_driver
    def new(self):
        #values needing to be reset per game
        global piece_num
        self.home_pieces = piece_num
        self.safe_pieces = 0
        self.live_pieces = 0
        self.safeboard = [0] * piece_num
        self.pieces = self.create_pieces(piece_num)

    def legal_moves(self,roll:int) -> list:
        out = []
        if roll == 6 and self.home_pieces > 0:
            #probable legal but we have to check for home square occupancy
            if board.board[self.home] == 0:
                #first block where a place is possible
                for piece in self.pieces:
                    #select a free piece to play (they are equivalent so the first will do)
                    if piece.status == 'home':
                        target_piece = piece #should always find one as home pieces is > 0
                        break
                if 'target_piece' not in locals():
                    print("target_pieces not defined, something has gone terribly wrong")
                newmove = Move(target_piece)
                #these defs are not technically needed but for clarity i'd rather have them
                newmove.capture = False #the tile is empty
                newmove.to_safe = False #can't move in the safe zone we put it on
                newmove.is_place = True
                out.append(newmove)
            else:
                #there is a piece on the home square
                if board.board[self.home].parent != self:
                    #second block, same as the first but it has to be nested like that cause i cant be bothered to do a try-except for the board members
                    for piece in self.pieces:
                        #select a free piece to play (they are equivalent so the first will do)
                        if piece.status == 'home':
                            target_piece = piece #should always find one as home pieces is > 0
                            break
                    if 'target_piece' not in locals():
                        print("target_pieces not defined, something has gone terribly wrong")
                    newmove = Move(target_piece)
                    newmove.capture = True #there is a piece on the tile and it's not ours
                    newmove.to_safe = False #can't move in the safe zone we put it on
                    newmove.is_place = True
                    out.append(newmove)
        #now that all possible placing moves are done we run through all the other pieces for any moves on the current roll
        for piece in self.pieces:
            if piece.status == 'live':
                if piece.position > piece.parent.terminator or piece.position + roll <= piece.parent.terminator:
                    #here we have all the live pieces we can iterate thru possible moves with
                    newmove = Move(piece)
                    if board.board[(piece.position + roll) % board_size] != 0: #if destination is occupied
                        if board.board[(piece.position + roll) % board_size].parent != self:
                            newmove.capture = True
                            #no need for an else clause as default is false
                        else:
                            continue #destination piece is own piece -> illegal move
                else:
                    #the if clause is set up for possible capturing moves that don't end up in the safe zone, hence 
                    if (piece.position + roll) - piece.parent.terminator <= piece_num and piece.parent.safeboard[(piece.position + roll)-(piece.parent.terminator + 1 )] == 0: #check to see if destination is on safe board
                        newmove = Move(piece)
                        newmove.to_safe = True
                    else:
                        continue #if the if check fails move is illegal
                out.append(newmove)
        for piece in self.pieces:
            if piece.status == 'safe':
                if piece.position + roll < piece_num and self.safeboard[piece.position+roll] == 0: #for legal safeboard move check if not OOB and space is empty
                    newmove = Move(piece)
                    out.append(newmove)
        return out
    def choice(self,moves,board:Board):
        #expects the moves list from legal_moves
        #returns the piece object desired to be moved
        return self.driver(self,moves,board)
    def move(self,piece,roll:int):
        if piece.status == 'home':
            board.place_piece(self)
        elif piece.status == 'live':
            board.move_piece(piece,roll)
        else:
            board.safe_move(self,piece,roll)

class Piece:
    def __init__(self,parent):
        self.position = -1 #-1 reserved for home location
        self.parent = parent #owner of piece
        self.status = 'home' #status of piece, i have to do this since there's no good way of handling the position with safe areas as they are a mess
        #NOTE: turned out to be a good way of having positions be context aware

class Move:
    #class for returning moves with a lot of properties
    #expects to be passed legal moves
    #due to quite a bit of edge cases, properties are set from legal_moves and not internally
    def __init__(self,piece):
        self.piece = piece
        self.capture = False
        self.to_safe = False
        self.is_place = False #is a new piece entering the board

print('select player count')
player_count = int(input())
board_size = 10 * player_count
print('enter pieces per player')
piece_num = int(input())
game = 0 #tracking
print('select sample size :\n')
sample_size = int(input())
methods = dir(clobrdo_methods)
methods = methods [8:] #slice first 8 entries which are __builtins__ of the module
print('Availible methods: ')
for i in range(len(methods)):
    print(i,' - ',methods[i])
Players = []
for i in range(player_count):
    print('Pick player ',i,'\'s driver.')
    driver = int(input())
    Players.append(Player(i,getattr(clobrdo_methods,methods[driver])))
try:
    #we want to be able to out any data even after a fatal
    while game < sample_size:
        #New game begins here
        board = Board()
        for player in Players:
            player.new()
            #reset to inital position     
        current_turn = 0 #we start at player 0
        turns = 0
        while board.winner == None: #run turns until winner is found
            '''TURN PHASE'''
            current_player = Players[current_turn]
            if current_player.live_pieces == 0:
                #NOTE: technically does not allow for moving in safe zone while no live pieces as a move 
                #roll three times and wait for a 6
                for x in range(3):
                    if random.randint(1,6) == 6:
                        board.place_piece(current_player) #legality not questioned as there are no player's live pieces to conflict
            else:
                roll = random.randint(1,6)
                possible_moves = current_player.legal_moves(roll)
                if possible_moves != []:
                    acting_piece = current_player.choice(possible_moves,board)
                    current_player.move(acting_piece,roll)
                if roll == 6: #second roll after a 6
                    roll = random.randint(1,6)
                    possible_moves = current_player.legal_moves(roll)
                    if possible_moves != []:
                        #there are moves to execute
                        acting_piece = current_player.choice(possible_moves,board)
                        current_player.move(acting_piece,roll)
            '''POST TURN PHASE'''
            current_turn = (current_turn + 1) % player_count #increment turn
            board.is_won(Players) # win check
            turns += 1 #new turn
        if game % 100 == 0:
            print('Player ',board.winner.turn_order,' won game ',game,'.')
        board.winner.wins += 1
        game += 1
except Exception as f:
    print(game,' games successfully ran')
    for player in Players:
        print('Player ',player.turn_order,' won ',player.wins,' games, for a total of ',100 *(player.wins/sample_size),'%')
    print('Press any key to exit')
    input()
    raise f
print(game,' games successfully ran')
for player in Players:
    print('Player ',player.turn_order,' won ',player.wins,' games, for a total of ',100 *(player.wins/sample_size),'%')
print('Press any key to exit')
input()