import Game
import Player
import Match
import random
import numpy as np

class GeneticAlgorithm:

    def __init__(self, n, maxGenerations, populationSize, mutationRate, game):
        self.n = n
        self.generations = maxGenerations
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.gamesPerMatch = 1000
        self.game = game

        temp = np.array(game.grid).flatten()
        self.minValue = min(temp)
        self.maxValue = max(temp)
        self.idealFitness = self.maxValue*self.gamesPerMatch-self.minValue*self.gamesPerMatch+1

    def mutate(self, player):
        strat = random.randint(0, 2)
        sign = random.randint(0, 1)  # 0 is add, 1 is subtract

        value = 0.05

        if(strat == 2): #coop
            if(sign ==0): #add
                player.setCoopValue(player.coop+value)
                player.setDefectValue(player.defect-value/2)
            else:
                player.setCoopValue(player.coop - value)
                player.setDefectValue(player.defect + value / 2)
        elif(strat == 1): #neutral
            if (sign == 0):  # add
                player.setCoopValue(player.coop - value/2)
                player.setDefectValue(player.defect - value/2)
            else:
                player.setCoopValue(player.coop + value / 2)
                player.setDefectValue(player.defect + value / 2)
        else: #defect
            if (sign == 0):  # add
                player.setCoopValue(player.coop - value / 2)
                player.setDefectValue(player.defect + value)
            else:
                player.setCoopValue(player.coop + value / 2)
                player.setDefectValue(player.defect - value)

        neutral = 1 - player.coop - player.defect

        while((player.coop > 1 or player.coop < 0) or (player.defect > 1 or player.defect < 0) or (neutral > 1 or neutral < 0)):
            if(player.coop > 1):
                player.setDefectValue(0)
                player.setCoopValue(1)
                return
            elif(player.defect > 1):
                player.setDefectValue(1)
                player.setCoopValue(0)
                return
            elif(neutral > 1):
                player.setDefectValue(0)
                player.setCoopValue(0)
                return

            if(player.coop < 0):
                player.setDefectValue(player.defect + -1*player.coop/2)
                player.setCoopValue(0)
            elif(player.defect < 0):
                player.setCoopValue(player.coop + -1*player.defect/2)
                player.setDefectValue(0)
            elif(neutral < 0):
                player.setCoopValue(player.coop + -1 * neutral / 2)
                player.setDefectValue(player.defect + -1 * neutral / 2)
            neutral = 1 - player.coop - player.defect


    def crossover(self, parent1, parent2, maxFit):
        if(maxFit/self.idealFitness > 0.95):
            crossed = []
            for i in range(self.n):
                c = (parent1[i].coop + parent2[i].coop)/2
                d = (parent1[i].defect+parent2[i].defect)/2
                crossed.append(Player.SetPlayer(0, c, d))

            return crossed
        else:
            index = random.randint(0, self.n-1)
            if(random.randint(0,1) == 0):
                return parent2[0:index-1] + parent1[index-1:]
            else:
                return parent1[0:index-1] + parent2[index-1:]

    def fitness(self, player):
        match = Match.Match(player, self.gamesPerMatch, self.game)
        value = max(match.playGame())
        self.game.resetGame()

        return (value - self.minValue*self.gamesPerMatch+1)

    def printOut(self, bestPlayer):
        string = "["
        for i in range(self.n):
            string += "(" + str(bestPlayer[i].coop) + "," + str(bestPlayer[i].defect) + "),"
        string += "]"
        return string

    def runGA(self):

        #define initial population
        population  = []
        fit = [0]*self.populationSize
        for i in range(self.populationSize):
            section = [None] * self.n
            for i in range(self.n):
                randomVariables = []
                random.uniform(0,1)
                a = random.uniform(0, 1)
                b = random.uniform(0, 1)

                r1 = min(a,b)
                r2 = max(a,b)

                section[i] = Player.SetPlayer(0, r1, r2-r1)
            population.append(section)

        # calculate initial fitness
        for j in range(self.populationSize):
            fit[j] = self.fitness(population[j])

        index = fit.index(max(fit))
        print("Best Player for initial:" + self.printOut(population[index]))
        print("Fitness for initial:" + str(fit[index]))

        #start iteration
        for i in range(self.generations):
            #generate self.populationSize offspring via crossover
            newPopulation = []
            sumFit = sum(fit)
            maxFit = max(fit)
            scaledFit = [fit[k]/sumFit for k in range(self.populationSize)]

            for j in range(self.populationSize):
                p1 = np.random.choice(self.populationSize, None, False, scaledFit)
                p2 = np.random.choice(self.populationSize, None, False, scaledFit)
                newPopulation.append(self.crossover(population[p1], population[p2], maxFit))

            #mutate the offspring
            for j in range(0,self.populationSize):
                for k in range(self.n):
                    self.mutate(newPopulation[j][k])

            #create new population
            population = newPopulation

            fit = [0] * self.populationSize
            #calculate fitness
            for j in range(self.populationSize):
                fit[j] = self.fitness(population[j])

            index = fit.index(max(fit))
            print("Best Player for generation #"+ str(i) + " :" + self.printOut(population[index]))
            print("Fitness for generation #" + str(i) + " :" + str(fit[index]))

            if(abs(fit[index] - self.idealFitness) < 0.0005):
                return i
        return self.generations