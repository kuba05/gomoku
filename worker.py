import copy
import threading

class Worker:
    def __init__(self, helper, board, legalMoves, playerOnPlay = 1, evaluation=0, lastMove=None):
        self.helper = helper
        self.board = copy.copy(board)
        self.legalMoves = copy.copy(legalMoves)
        self.evaluation = {"evaluation": evaluation, "move": lastMove, "kids": {}, "sortedKids": []}
        self.moves = []
        self.playerOnPlay = 1 if playerOnPlay == 1 else 2
        self.working = False
        self.lock = False
        self.bestLine = []
        self.movesQueue = []
        self.playedMoves = []
        
    def _createNode(self, move):
        currentEval = self.getCurrentEvaluation()
        currentEval["sortedKids"].append(move)
        currentEval["kids"][self.helper.getArrayHash(move)] = {"evaluation": -currentEval["evaluation"], "move": move, "kids": {}, "sortedKids": []}
    
    def playMove(self, move):
        if self.lock:
            print("locked")
            self.movesQueue.append(move)
            return
            
        self.playedMoves.append(move)
        self._prepareLevel()
        self._navigate(move)
        self.evaluation = self.getCurrentEvaluation()
        self.moves = self.moves[1:]
    def _navigate(self, move):
        """
            move in nodes tree
        """
        #go level up
        if move == "..":
            lastMove = self.moves.pop()
            self.helper.setField(self.board, lastMove, 0)
            self.legalMoves.append(lastMove)
            
        #go deeper
        else:
            self.moves.append(move)
            self.helper.setField(self.board, move, self.playerOnPlay)
            self.legalMoves.remove(move)

        #always change who's on play
        self.playerOnPlay = self.playerOnPlay % 2 + 1
            
    def _evaluate(self):
        """
            evaluate current node
        """
        #TODO use real evaluation
        currentEval = self.getCurrentEvaluation()
        currentEval["evaluation"] += self.helper.evaluateMove(self.board, currentEval["move"], self.playerOnPlay)
        
    def _work(self):
        """
            start async working until stoping Object id
            
        """
        self.lock = True
        while self.working:
            self.goDeeper()
            self.calculateBestLine()
        self.lock = False
        #empty stacked moves
        print("playing the queue")
        for move in self.movesQueue:
            self.playMove(move)
        self.movesQueue = []
            
    def startWorking(self):
        self.working = True
        print("creating Thread")
        work = threading.Thread(target = self._work)
        print(work)
        work.start()
        
    def stopWorking(self):
        self.working = False
        
    def getCurrentEvaluation(self):
        """
            get evaluation of current node
        """
        current = self.evaluation
        for move in self.moves:
            current = current["kids"][self.helper.getArrayHash(move)]
        return current
        
    def _sortCurrentKidsAndChangeEval(self):
        """
            sort all kids of current node by their current evaluation and change the evaluation of the current node
        
        Move eval has the format:
            [move, eval, [[othermove, eval, []]...]]
        """
        currentEval = self.getCurrentEvaluation()
        
        def sortHelper(move):
            return currentEval["kids"][self.helper.getArrayHash(move)]["evaluation"]
            
        #minimalize the opponent's advantage after our move
        currentEval["sortedKids"].sort(reverse = False, key = sortHelper)
       
        	#the better the position is for our opponent, the worse it os for us
        currentEval["evaluation"] = -1 * currentEval["kids"][self.helper.getArrayHash(currentEval["sortedKids"][0])]["evaluation"]
        
    def _prepareLevel(self):
        """
            make kids and change evaluation of current node
        """
        #print("kids made")
        #print(len(self.legalMoves))
        for move in copy.copy(self.legalMoves):
            self._createNode(move)
            self._navigate(move)
            self._evaluate()
            self._navigate("..")
        self._sortCurrentKidsAndChangeEval()
        #cut down the number of lines
        self.getCurrentEvaluation()["sortedKids"] = self.getCurrentEvaluation()["sortedKids"][:6]
        
    def goDeeper(self):
        """
            go one level deeper in the best line
        """
        #how many lines should be calculated
        currentEval = self.getCurrentEvaluation()
        #print(self.moves)
        #if the current node has no child, create kids for it
        if len(currentEval["sortedKids"]) == 0:
            self._prepareLevel()
        #if it has some, continue in the best one
        else:
            self._navigate(currentEval["sortedKids"][0])
            self.goDeeper()
            self._navigate("..")
        self._sortCurrentKidsAndChangeEval()
        
    def calculateBestLine(self):
        moves = 0
        while len(self.getCurrentEvaluation()["sortedKids"]) != 0:
            self._navigate(self.getCurrentEvaluation()["sortedKids"][0])
            moves += 1
        output = copy.copy(self.moves)
        for i in range(moves):
            self._navigate("..")
        self.bestLine = output

    def getBestLine(self):
        return self.bestLine