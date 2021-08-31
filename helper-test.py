from helper import Helper

helper = Helper()

def testHashes():
    h = helper.getArrayHash

    allHashes = []

    good = True
    
    a = [[i,j] for i in range(15) for j in range(15)]
    print(len(a))
    for array in a:
        x=h(array)
        if x in allHashes:
            print("error")
            good = False
        allHashes.append(x)
    
    print(good)

def testEval():
    board = [[0 for i in range(15)] for j in range(15)]
    board[7][7] = 2
    board[8][7] = 1
    print(helper.evaluateMove(board, [8,8], 1))

def testThreatEval():
    good = True
    for length in range(5):
        for ends in range(1,3):
            good = good and 10**(length + ends + 1) == helper.evaluateThreat(length, ends, True)
    for length in range(5):
        for ends in range(1,3):
            good = good and -(10**(length + ends)) == helper.evaluateThreat(length, ends, False)
    
    print(good)
    
testHashes()
testThreatEval()

testEval()
