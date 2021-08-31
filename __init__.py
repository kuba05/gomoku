from worker import Worker
from helper import Helper

import time

"""
Constants. Feel free to overwrite them!
"""

BOARD_SIZE = 15
STARTING_LETTER = 'a'
CALCULATE_SPEED = True




#creating worker
helper = Helper(gatherData = CALCULATE_SPEED)
worker = Worker(helper, [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)], [[i,j] for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)])

def parseFromLetter(letter):
    """
        parse a letter into a number
    """
    return ord(letter) - ord(STARTING_LETTER)
    
def parseToLetter(number):
    """
        parse a number into a letter
    """
    return chr(number + ord(STARTING_LETTER))
    
    
def playMove():
    
    if CALCULATE_SPEED:
        startingTime = time.time()
        startingNodes = helper.getNodes()
    #start computing the move
    worker.startWorking()
    
    #wait for signal to make a move
    input()
   
    #output the move
    bestLine = worker.getBestLine()
    print(worker.playedMoves + bestLine)
    move = bestLine[0]
    print( '!' + parseToLetter(move[0]) + str(move[1] + 1) )
    
    #play the move()
    worker.playMove(move)
    worker.stopWorking()
    
    if CALCULATE_SPEED:
        t = time.time()-startingTime
        nodes = helper.getNodes() - startingNodes
        print(nodes/t, "nodes/s")

def readMove():
    """
        Read a move from stdin and, provided there is a move, play it on the worker.
        
        Move has to have to following format:
            !XY
        where X is a letter, signalizing the file, and Y is an integer with any number of digits, signalizing the row.
        
        If a move is found, return code is 0. Otherwise it's 1.
    """
    move = input()
    
    #the input is a move
    if len(move) > 0 and move[0] == '!':
        #read and play the move
        try:
            worker.playMove([parseFromLetter(move[1]), int(move[2:])-1])
        except ValueError as e:
            print(e)
            return 1
        return 0
    return 1
    
    
#opening

#if read move had an error (it have not read a move)
if readMove():
    
    #play the pre-defined move
    print( '!' + parseToLetter(int(BOARD_SIZE / 2)) + str( int(BOARD_SIZE / 2) + 1 ) )
    worker.playMove([int(BOARD_SIZE / 2), int(BOARD_SIZE / 2)])
   
    #read input until there's a valid move
    while readMove():
        pass
else:
    #if the move was valid, we are the second to play
    
    #play the pre-defined move
    print( '!' + parseToLetter(int(BOARD_SIZE / 2) + 1) + str( int(BOARD_SIZE / 2) + 2 ) )
    worker.playMove([int(BOARD_SIZE / 2) + 1, int(BOARD_SIZE / 2) + 1])
    
    #read input until there's a valid move
    while readMove():
        pass
        
#gameloop
while True:
    playMove()
    
    #read imput untill there's a valid move
    while readMove():
        pass
    