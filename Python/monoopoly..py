import random

#type,name
#type = [normal property, railroad, utilities, carddraws, special]
board = [
    [5,'Go',0], #special = Go,Income Tax, Jail, Free parking, Go to jail, Luxury tax
    [0,'Old Kent Road',60,[2,10,30,90,160,250]], #normal properties have buy cost + rent rows
    [4,'Community Chest',0],
    [0,'Whitechapel Road',60,[4,20,60,180,320,450]],
    [5,'Income Tax',1],
    [1,'Kings Cross Station'], #railroads behave the same so no need to store costs
    [0,'The Angel Islington',100,[6,30,90,270,400,550]],
    [4,'Chance',1],
    [0,'Euston Road',100,[6,30,90,270,400,550]],
    [0,'Pentonville Road',120,[8,40,100.300,450,600]],
    [5,'Jail',2],
    [0,'Pall Mall',140,[10,50,150,450,625,750]],
    [3,'Electric company'], #both cost 150 so eh
    [0,'Whitehall',140,[10,50,150,450,625,750]],
    [0,'Northumberland Avenue',160,[12,60,180,500,700,900]],
    [1,'Marleybone Station'],
    [0,'Bow Street',180,[14,70,200,550,750,950]],
    [4,'Community Chest',0],
    [0,'Marlborough Street',180,[14,70,200,550,750,950]],
    [0,'Vine Street',200,[16,80,220,600,800,1000]],
    [5,'Free Parking',3],
    [0,'The Strand',220,[18,90,250,700,875,1050]],
    [4,'Chance',1],
    [0,'Fleet Street',220,[18,90,250,700,875,1050]],
    [0,'Trafalgar Square',240,[20,100,300,750,925,1100]],
    [1,'Fenchurch St Station'],
    [0,'Leicester Square',260,[22,110,330,800,975,1150]],
    [0,'Coventry Street',260,[22,110,330,800,975,1150]],
    [3,'Water Works'],
    [0,'Piccadilly',280,[24,250,360,850,1025,1200]],
    [5,'Go To Jail',4],
    [0,'Regent Street',300,[26,130,390,900,1100,1275]],
    [0,'Oxford Street',300,[26,130,390,900,1100,1275]],
    [4,'Community Chest',0],
    [0,'Bond Street',320,[28,150,450,1000,1200,1400]],
    [1,'Liverpool Street Station'],
    [4,'Chance',1],
    [0,'Park Lane',350,[35,175,500,1100,1300,1500]],
    [5,'Luxury Tax',5],
    [0,'Mayfair',400,[50,200,600,1400,1700,2000]]
]

class player():
    def __init__(self,playernum):
        self.turnorder = playernum
        self.money = 1500
        self.owned_props = []
        self.cards = []
        self.pos = 0 #go square

class prop():
    def __init__(self,lst):
        self.pos = lst[0]
        self.owner = 0 #0 is nobody
        self.houses = 0
        self.morgaged = False
        self.buy = lst[2]


        



'''def get_pos(num): #get what a tile does of its position
    return [tile_type,details]'''

def roll_dice():
    rolls = 0 # #of rolls
    roll = 0  #number thrown
    while rolls <3:
        rolls+=1
        roll_1 = random.randint(1,6)
        roll_2 = random.randint(1,6)
        roll += roll_1
        roll += roll_2
        if roll_1 == roll_2:
            continue
        else:
            break
        return 0 #jail
    return roll

def buy_property(player):
    global turn
    p = prop(board[player.pos])
    
'''
TODO:Flags for when buying props can even be considered
TURN ORDER:
Check if you passed go (happens every turn)
    Choices availible every time
Then one of these will happen:
    - Nothing (standing on ur property or free parking or jail visit)
    - Stand on vacant property
    - Stand on enemy property
    - Draw card
    - Pay a tax
    - Be in Jail
    - Go to Jail



'''

if __name__ == "__main__":
    turn = 1 #whose players turn is it
    player1 = player(1)
    player2 = player(2)
    for i in range(len(board)):
