#-*-coding:utf8;-*-
#qpy:3
#qpy:console

class InvalidPosition(IndexError):
    pass

class Helper:
    
    def __init__(self, *void, gatherData = False):
        """
            if gatherData is true, every time an attribute or method of Helepr is accessed, the access is logged
        """
        self.evaluateMove = self.gomokuEvaluateMove
        self.nodes = 0
        
        self.gatherData = gatherData
            
            
    def getNodes(self):
        return self.nodes
        
    def getDirections(self):
        """
        returns the direction for each row, column and diagonal
        """
        return [[1,0],[1,1],[0,1],[-1,1]]

    def getArrayHash(self, array):
        if len(array) == 0:
            return 0
        x = self.getArrayHash(array[1:])
        return int((array[0]+x)*(array[0]+x+1)/2 + 1 + array[0])
    
    
    def multiplyArrays(self, arrayA, arrayB):
        """
        if arrays are of the same size, returns new array that is the multiply
        """
        if len(arrayA) != len(arrayB):
            return null
        return [arrayA[i] * arrayB[i] for i in range(len(arrayA))]


    def multiplyArray(self, arrayA, constant):
        """
        multiplies array by a number
        """
        return [arrayA[i] * constant for i in range(len(arrayA))]
    
    
    def addArrays(self, arrayA, arrayB):
        """
        if arrays are of the same size, returns new array that is the additiom
        """
        if len(arrayA) != len(arrayB):
            return null
        return [arrayA[i] + arrayB[i] for i in range(len(arrayA))]
    
    
    def getField(self, board, position):
        """
        get a field on given position
        """
        if position[0] >= len(board) or position[1] >= len(board[0]):
            raise InvalidPosition()
        return board[position[0]][position[1]]
      
        
    def setField(self, board, position, value):
        """
            set a field on given board to the given value
        """
        board[position[0]][position[1]] = value
      
    def evaluateThreat(self, lengthOfThreat, numberOfFreeEnds, isThePlayerOnPlay):
        """
            positive eval is good for playerOnPlay
        """
        evaluation = 0
        if numberOfFreeEnds == 0:
            evaluation = 0
        elif isThePlayerOnPlay:
            evaluation = 10**(lengthOfThreat + numberOfFreeEnds + 1)
        else:
            evaluation = - 10**(lengthOfThreat + numberOfFreeEnds)
        return evaluation
        
    def gomokuEvaluateMove(self, board, move, playerOnPlay):
        """
            playerOnPlay is the one, who has not played the evaluated move
            
            positive eval is good for playerOnPlay
        """
        if self.gatherData:
            self.nodes += 1
        evaluation = 0
        
        #look at all directions
        for direction in self.getDirections():
            
            totalOpenEnds = 0
            #the piece that was just played has to be counted as well
            totalLength = 1
            
            #cycle both ways
            for i in range(2):
                
                length = 1
                openEnds = 0
                
                #set the threat owner
                try:
                    position = self.addArrays(move, direction)
                    threatOwner = self.getField(board, position)
                except InvalidPosition:
                    #the field doesn't exist, therefore it is not an open end nor does it advance the threat
                    break
                #if the field is empty, it doesn't help the threat
                #but it means the threat consisting of the last played move does have an open end
                if threatOwner == 0:
                    totalOpenEnds += 1
                    #try the other direction
                else:
                
                    #expand the threat
                    while True:
                        try:
                            field = self.getField(board, self.addArrays(move, self.multiplyArray(direction, length)))
                        except InvalidPosition:
                            #the field doesn't exist, therefore it is not an open end nor does it advance the threat
                            break
                        if field == threatOwner:
                            length += 1
                        else:
                            if field == 0:
                                openEnds += 1
                            break
                        
                #switch the directiom
                direction = self.multiplyArray(direction, -1)
    
                #evaluate threat if it's of the player who just made a move
                if threatOwner != playerOnPlay:
                    evaluation -= self.evaluateThreat(length, openEnds+1, False)
                    totalLength += length
                    totalOpenEnds += openEnds
                    continue
                
                #change the evaluation if the threat is of the player on play
                evaluation -= self.evaluateThreat(length, openEnds+1, True)
                evaluation += self.evaluateThreat(length, openEnds, True)
                
            #evaluate threat of the player, who just made a move
            evaluation += self.evaluateThreat(totalLength, totalOpenEnds, False)
        
        return evaluation
        
    def testEvaluateMove(self, board, move, player):
        """
            playerOnMove is the one, who has not played the evaluated move
            
            positive eval is good for playerOnMove
        """
        
        return 0-move[0]-move[1]