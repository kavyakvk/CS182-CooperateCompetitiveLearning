import copy
import math

class Game:

    def retrieveValue(self, indexArr, playerNum):
        if(self.name == "EPD"):
            return self.retrieveEPDValue(indexArr, playerNum)
        else:
            return self.retrieveExplicitValue(indexArr, playerNum)

    def retrieveEPDValue(self, indexArr, playerNum):
        k = sum(indexArr)
        societalValue = (((200.0)/(2*self.n))*k)-100
        base = societalValue / self.n

        playerStrat = indexArr[playerNum]
        numZero = indexArr.count(0)
        numTwo = indexArr.count(2)

        bonus = 25 + math.floor(100.0 / (1 +k))

        if(k == 0):
            return (-100.0)/self.n #everyone defects
        elif(k == 2*self.n):
            return (100.0)/self.n #everyone cooperates

        if (playerStrat == 1):
            if((numZero == 0)and(numTwo == 0)):
                return base
            elif(numTwo == 0):
                return base - bonus / numZero
            else:
                return base + bonus / numTwo
        elif (playerStrat == 0):
            return base + bonus / numZero
        else:
            return base - bonus / numTwo

    def retrieveExplicitValue(self, indexArr, playerNum):
        tempGrid = copy.deepcopy(self.grid)
        for i in range(self.n):
            t = indexArr[i]
            tempGrid = tempGrid[t]
        return tempGrid[playerNum]

    def editValue(self, indexArr, playerNum, val):
        tempGrid = self.grid
        for i in range(self.n):
            t = indexArr[i]
            tempGrid = tempGrid[t]
        tempGrid[playerNum] = val

    def generateEPDGrid(self):
        def initializeGrid(tempN, n):
            if(tempN==0):
                return [0 for i in range(n)]
            else:
                newArr = [0 for i in range(3)]
                for i in range(3):
                    newArr[i] = initializeGrid(tempN-1, n)
                return newArr

        self.grid = initializeGrid(self.n, self.n)

        def fillGrid(tempGrid, indexArr, n):
            if(len(indexArr) == n):

                for i in range(n):
                    self.editValue(indexArr, i, self.retrieveEPDValue(indexArr, i))
            else:
                for j in range(3):
                    nextTempGrid = tempGrid[j]
                    nextIndexArr = copy.deepcopy(indexArr)
                    nextIndexArr.append(j)
                    fillGrid(nextTempGrid, nextIndexArr, n)

        emptyArray = list()
        fillGrid(self.grid, emptyArray, self.n)

    def __init__(self, n, name, payoffGrid):
        self.n = n
        self.name = name

        self.grid = None
        if(self.name == "EPD"):
            self.generateEPDGrid()
        else:
            self.grid = payoffGrid

        self.scores = [0 for i in range(self.n)]
        self.gamestate = []

    def getPlayerCount(self):
        return self.n

    def getPayoff(self, stratArr, player):
        return self.retrieveValue(stratArr, player)

    def updateGame(self,  strategy):
        stratArr = []
        for player in range(len(strategy)):
            self.gamestate.append(strategy[player])
            stratArr.append(strategy[player])

        for i in range(self.n):
            self.scores[i] = self.scores[i] + self.getPayoff(stratArr, i)

    def playByPlay(self, turnCount):
        return

    def lastTurn(self):
        return self.gamestate[-self.n:]

    def playerXMoves(self, player):
        output = []
        playerCount = len(self.scores)
        turnCount = len(self.gamestate) / playerCount
        for turn in range(turnCount):
            strat = self.gamestate[turn*playerCount + player]
            strategy = []
            for plays in range(playerCount):
                strategy.append(self.gamestate[turn*playerCount + plays])
            score = self.getPayoff(strategy, player)
            output.append((strat, score))
        return output

    def resetGame(self):
        self.scores = [0 for i in range(self.n)]
        self.gamestate = []