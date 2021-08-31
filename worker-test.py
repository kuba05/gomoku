from worker import Worker
import code
import time
from helper import Helper

helper = Helper()
field = [[0 for i in range(15)] for j in range(15)]
moves = [[i,j] for i in range(15) for j in range(15)]
w = Worker(helper, field, moves, 10)

e = w.getCurrentEvaluation

l = w.getBestLine

c = w.calculateBestLine

makeMove = w.playMove

work = w.startWorking

stop = w.stopWorking

makeMove([7,7])
makeMove([8,7])

work()
time.sleep(2)
stop()

code.interact(local = locals())

