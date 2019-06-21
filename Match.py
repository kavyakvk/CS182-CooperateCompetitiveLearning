class Match:

    def __init__(self, players, turnCount, game):
        self.players = players
        self.turnCount = turnCount
        self.game = game

        for i in self.players:
            i.setGrid(self.game.grid)

    def move(self):
        strategy = []
        for player in self.players:
            if(len(self.game.gamestate) == 0):
                strategy.append(player.strategy(None, self.game.scores))
            else:
                strategy.append(player.strategy(self.game.lastTurn(), self.game.scores[player.playerNumber]))
        self.game.updateGame(strategy)
        return self.game.scores

    def learningMove(self, learningPlayer):
        strategy = []
        for player in self.players:
            if(len(self.game.gamestate) == 0):
                strategy.append(player.strategy(None, self.game.scores))
            else:
                strategy.append(player.strategy(self.game.lastTurn(), self.game.scores[player.playerNumber]))
        self.game.updateGame(strategy)
        reward = self.game.getPayoff(strategy, learningPlayer)
        return (strategy, reward)

    def playGame(self):
        for i in range(self.turnCount):
            self.move()
        return(self.game.scores)

    def playLearningMatch(self, learningPlayer):
        turns = []
        payoffs = []
        for i in range(self.turnCount):
            output = self.learningMove(learningPlayer)
            turns.append(output[0])
            payoffs.append(output[1])
        return (turns, payoffs)