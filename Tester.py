import Game
import Player
import Match
import GeneticAlgorithm
import csv
import random
from copy import deepcopy

from itertools import combinations_with_replacement

def GA():

    with open("GAoutput1.csv", "wb") as f:
        writer = csv.writer(f)

        maxGenerations = 3000
        #sectionSize = [50, 100, 150, 200, 250, 300]
        #mutationRate = [0.03, 0.05, 0.07, 0.09]
        populationSize = [250, 500, 750]
        mutationRate = [0.07, 0.09, 0.11]
        nVals = [5, 6, 7]

        writer.writerow(["Section Size", "Changing Mutation Rate", "Generations till Solution"])
        for m in mutationRate:
            s = 250
            n = 6
            game = Game.Game(n, "EPD", None)
            ga = GeneticAlgorithm.GeneticAlgorithm(n, maxGenerations, s, m, game)
            print(ga.idealFitness)
            generations = ga.runGA()
            game.resetGame()

            result = [str(s), str(m), str(generations)]
            writer.writerow(result)

        writer.writerow(["Changing Section Size", "Mutation Rate", "Generations till Solution"])
        for s in populationSize:
            m = 0.09
            n = 6
            game = Game.Game(n, "EPD", None)
            ga = GeneticAlgorithm.GeneticAlgorithm(n, maxGenerations, s, m, game)
            print(ga.idealFitness)
            generations = ga.runGA()
            game.resetGame()

            result = [str(s), str(m), str(generations)]
            writer.writerow(result)

def createMatch(players):
    n = len(players)

    game = Game.Game(n, "EPD", None)
    players1 = players
    match1 = Match.Match(players1, 1000, game)
    results1 = match1.playGame()

    print("\nRandom player in position 0")
    ind = 0
    for i in range(len(results1)):
        if results1[i] > results1[ind]:
            ind = i
    print("winner is: " + str(ind))
    print(results1)

    game = Game.Game(n, "EPD", None)
    playersTraining = players
    AI = Player.LearningAgent(0, game)

    # Training the AI
    for i in range(500):
        game = Game.Game(n, "EPD", None)
        matchTraining = Match.Match(playersTraining, 1000, game)
        output = matchTraining.playLearningMatch(0)
        AI.updateQScores(output, 0)

    # Testing the AI
    game = Game.Game(n, "EPD", None)
    players2 = playersTraining
    players2[0] = AI

    for i in range(n):
        if(players2[i].playerName == "ExpertLearningPlayer"):
            players2[i].stopLearning()

    match2 = Match.Match(players2, 1000, game)
    results2 = match2.playGame()

    print("\nAI player in position 0")
    ind = 0
    for i in range(len(results2)):
        if results2[i] > results2[ind]:
            ind = i
    print("winner is: " + str(ind))
    print(results2)


    #comparing to expert learning
    game = Game.Game(n, "EPD", None)

    players3 = players2
    players3[0] = Player.ExpertAdvicePlayer(0, game)

    match3 = Match.Match(players3, 1000, game)
    results3 = match3.playGame()

    print("\nEL player in position 0")
    ind = 0
    for i in range(len(results3)):
        if results3[i] > results3[ind]:
            ind = i
    print("winner is: " + str(ind))
    print(results3)

    answer = [str(results1), str(results2), str(results3)]

    if(max(results2) == results2[0]):
        answer = answer + ["1"]
    else:
        answer = answer + ["0"]

    if (max(results3) == results3[0]):
        answer = answer + ["1"]
    else:
        answer = answer + ["0"]

    answer = answer + [str(results1[0]), str(results2[0]), str(results3[0])]

    return answer

def matchCombinations():
    with open("PlayersSecond.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerow(["Combination of Players", "Scores with Random in 0", "Scores with AI in 0", "Scores with EL in 0", "AI Won?", "EL Won?", "Random Score for Game 1", "AI Score for Game 2", "EL Score for Game 3"])
        n = 6

        game = Game.Game(n, "EPD", None)

        p1 = Player.SetPlayer(0, 0.1, 0.8)  # Defector
        p2 = Player.TitForTatPlayer(1, 0.3)
        p3 = Player.RandomPlayer(2)
        p4 = Player.SetPlayer(3, 0.8, 0.1)  # Cooperative
        p5 = Player.ExpertAdvicePlayer(4, game)

        allPlayers = [p1, p2, p3, p4, p5]

        comb = list(combinations_with_replacement(allPlayers, 5))

        for i in range(len(comb)):
            playersTuple = comb[i]

            players = [Player.RandomPlayer(0)]
            for j in range(len(playersTuple)):
                a = deepcopy(playersTuple[j])
                a.setPlayerNumber(j+1)
                players.append(a)


            playersString = ""
            for j in range(1, len(players)):
                playersString += (players[j].playerName + "; ")
            print(playersString)

            results = createMatch(players)

            print(max(results))

            output = [playersString] + results

            writer.writerow(output)

if __name__ == '__main__':
    #game = Game.Game(2, "EPD", None)
    #print(game.grid)
    GA()

    #matchCombinations()