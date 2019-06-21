import random
import math
import copy

class Player:
    grid = None
    playerNumber = None

    def __init__(self, playerNumber):
        self.playerNumber = playerNumber
        self.playerName = "Generic"

    def strategy(self, lastTurn, playerScore):
        pass

    def setGrid(self, grid):
        self.grid = grid

    def setPlayerNumber(self, num):
        self.playerNumber = num

class RandomPlayer(Player):
    def __init__(self, playerNumber):
        self.playerNumber = playerNumber
        self.playerName = "Random"
    def strategy(self, lastTurn, playerScore):
        return random.randint(0, 2)

class SetPlayer(Player):
    def __init__(self, playerNumber, coop, defect):
        self.playerNumber = playerNumber
        self.coop = coop
        self.defect = defect
        self.playerName = "SetPlayer " + str(coop) + "," +str(defect)

    def strategy(self, lastTurn, playerScore):
        rand = random.uniform(0, 1)
        if(rand < self.coop):
            return 2
        if (rand > self.coop and rand < self.coop + self.defect):
            return 0
        else:
            return 1
    def setCoopValue(self, value):
        self.coop = value
    def setDefectValue(self, value):
        self.defect = value
class TitForTatPlayer(Player):

    def __init__(self, playerNumber, alpha):
        self.playerNumber = playerNumber
        self.alpha = alpha
        self.playerName = "TitForTat"
    def strategy(self, lastTurn, playerScore):
        if(lastTurn == None):
            return 0

        del lastTurn[self.playerNumber]
        mostCommon = max(set(lastTurn), key=lastTurn.count)

        return mostCommon

class ExpertAdvicePlayer(Player):

        def __init__(self, playerNumber, game):
            self.playerNumber = playerNumber
            self.playerName = "ExpertLearningPlayer"
            self.game = game
            self.weights = [1 for i in range(self.game.n)]
            self.weights[self.playerNumber] = 0
            self.cumL = [0 for i in range(self.game.n)]

            self.learningRate = 0.2
            self.randomness = 0.05

            self.learning = True

        def stopLearning(self):
            self.learning = False

        def strategy(self, lastTurn, playerScore):

            if (lastTurn == None):
                return 2

            def Loss(y, maxReward, minReward):
                return (y-minReward)/maxReward

            if(self.learning == True):
                n = len(lastTurn)
                k = sum(lastTurn) - lastTurn[self.playerNumber]

                minReward = ((((200.0)/(2*n))*k)-100)/n + (25 + math.floor(100.0 / (1 + 2)))  # when one cooperates and everyone else defects
                maxReward = ((((200.0)/(2*n))*k)-100)/n - (25 + math.floor(100.0 / (1 + (2 * n - 2))) ) # when one defects and everyone else cooperates

                loss = []
                for i in range(self.game.n):
                    loss.append(Loss(self.game.retrieveValue(lastTurn, i), maxReward, minReward))
                    self.cumL[i] += loss[i]

                # R = self.cumL[self.playerNumber] - min(self.cumL)

                num = 0.0
                denom = 0.0
                for i in range(self.game.n):
                    if (i != self.playerNumber):
                        num += self.weights[i] * lastTurn[i]
                        denom += self.weights[i]

                predict = num / denom

                for i in range(self.game.n):
                    if (i != self.playerNumber):
                        self.weights[i] = self.weights[i] * math.exp(-1 * self.learningRate * loss[i])

                norm = [i / sum(self.weights) for i in self.weights]
                self.weights = norm

                strat = int(round(predict))

                rand = random.uniform(0, 1)

                others = [0,1,2]
                others.remove(strat)

                if (rand > self.randomness * 2):
                    return strat
                elif (rand <= self.randomness):
                    return others[0]
                else:
                    return others[1]
            else:
                num = 0.0
                denom = 0.0
                for i in range(self.game.n):
                    if (i != self.playerNumber):
                        num += self.weights[i] * lastTurn[i]
                        denom += self.weights[i]

                predict = num / denom

                strat = int(round(predict))

                rand = random.uniform(0, 1)

                others = [0, 1, 2]
                others.remove(strat)

                if (rand > self.randomness * 2):
                    return strat
                elif (rand <= self.randomness):
                    return others[0]
                else:
                    return others[1]

class LearningAgent(Player):

    def __init__(self, playerNumber, game):
        self.playerNumber = playerNumber
        self.game = game
        self.playerCount = self.game.getPlayerCount()
        self.QStates = {}
        self.learningRate = 0.2
        self.discount = 0.8
        self.fillQStates()
        self.playerName = "LearningAgentPlayer"

    def strategy(self, lastTurn, playerScore):
        # lastTurn includes what this player did
        if lastTurn != None:
            key = ""
            for i in range(len(lastTurn)):
                key = key + str(lastTurn[i])
            key0 = copy.deepcopy(key)
            key1 = copy.deepcopy(key)
            key2 = copy.deepcopy(key)
            key0 = key0 + "0"
            key1 = key1 + "1"
            key2 = key2 + "2"
            val0 = self.QStates[key0]
            val1 = self.QStates[key1]
            val2 = self.QStates[key2]
            if val0 >= val1 and val0 >= val2:
                return 0
            if val1 >= val2:
                return 1
            return 2
        else:
            return random.randint(0, 2)

    def fillQStates(self):
        def ex3(n):
            answer = 1
            for i in range(n):
                answer = answer * 3
            return answer
        count = ex3(self.playerCount)
        for num in range(count):
            strindex = ""
            for digit in range(self.playerCount):
                strindex = strindex + str((int((num % ex3(digit+1)) / (ex3(digit)))))

            key0 = copy.deepcopy(strindex) + "0"
            key1 = copy.deepcopy(strindex) + "1"
            key2 = copy.deepcopy(strindex) + "2"
            self.QStates[key0] = 0.0
            self.QStates[key1] = 0.0
            self.QStates[key2] = 0.0

    def updateQScore(self, qState, currentReward, nextState):

        key = ""
        for i in range(len(qState[0])):
            key = key + str(qState[0][i])
        key = key + str(qState[1])
        currQS = self.QStates[key]
        key2 = ""
        if nextState != None:
            for i in range(len(nextState)):
                key2 = key2 + str(nextState[i])
            a0 = self.QStates[key2 + "0"]
            a1 = self.QStates[key2 + "1"]
            a2 = self.QStates[key2 + "2"]
            maxAction = max(a0, a1, a2)
            update = ((1-self.learningRate)*currQS) + (self.learningRate*((self.discount*maxAction) + currentReward))
        else:
            update = ((1 - self.learningRate) * currQS) + (self.learningRate * currentReward)
        if abs(update) > 1000000:
            self.rescaleQValues()
        self.QStates[key] = update

    def updateQScores(self, match, playerNumber):
        # A match is a sequence of turns [[p11,p21,...p1n],...,[pk1,pk2,...pkn]]
        # followed by a sequence of payoffs (P1,P2,...Pk) that playerNumber received

        turnCount = len(match[0]) # or alternatively equal len(match[1]) by definition of match
        for turn in range(turnCount):
            # Update the Q-state defined by
            currentTurn = match[0][turn]
            currentAction = currentTurn[playerNumber]
            currentReward = match[1][turn]
            qState = (currentTurn, currentAction)
            next = None
            if turn != turnCount - 1:
                next = match[0][turn+1]
            self.updateQScore(qState, currentReward, next)

    def rescaleQValues(self):
        keys = self.QStates.keys()
        max = 0.0
        for key in keys:
            if abs(self.QStates[key]) > max:
                max = abs(self.QStates[key])
        scalar = 100.0 / max
        for key in keys:
            self.QStates[key] = self.QStates[key] * scalar