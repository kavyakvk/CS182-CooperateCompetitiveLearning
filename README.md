# CoperativeCompetitiveLearning
Cooperative and Competitive Learning Agents in games with Non Pareto Optimal Nash Equilibria

## Project Overview

In this project, we pose two separate ”games” to play, one which naturally encourages com- petition and one which encourages cooperation, and observe the interactions between players in these situations.

The competitive game, which we call the Extended Prisoner’s Dilemma (EPD), resembles the Prisoner’s Dilemma but is extended to three possible strategies (cooperate, neutral, and defect), and any number of players. In this game, defecting against cooperating players leads to higher personal utility but lower societal utility. To play this game, we defined several set-strategy play- ers, such as a Random Player, a Cooperative Player, a Tit For Tat Player, and a Greedy Defector Player. We also implemented an Expert Learner, which determines its strategy through a weighted sum of the other players strategy, increasing weights on successful players over time while decreasing the weight of unsuccessful players. Finally, we developed a variant of reinforcement learning, random reinforcement learning (RRL), to learn a strategy to play this game through the
observation of other players playing the game.

The cooperative game, based off a game played in Harvard’s Psych 15 class and a version of the Tragedy of the Commons, models a situation where cooperating with other players leads to maximum utility for all. To determine the optimal combination of players to successfully play this cooperative game, we employed a modified genetic algorithm (GA) to adjust cooperation/neutral/defect tendencies of a group of players playing the game together.


## System Description
The file necessary to run the project can be found in Tester.py. The main method at the bottom of the file contains 4 lines of code:

- The first two demonstrate the generation of a game grid with two players and prints it out. The number can be modified to demonstrate that our program can automatically generate payoff matricies for any number of players. 
- The third line, GA(), runs the genetic algorithm experiment detailed in Section 5.2.
- The last line, matchCombinations(), runs the RRL experiment testing every combination of players with the RRL Agent learning scheme detailed in Section 5.1. 

These three commands encompass the major functions created for this project. The classes created for this project include:
- Player: Contains the code for the implementation of the 3 fixed-strategy players (RandomPlayer, SetPlayer, and TitForTatPlayer), the Expert Learner, and the RRL Agent. Each of these players are classes which extend the abstract class Player. 
- Game: Contains the code for playing one round of a Match and calculating the payoff. The Game can be played using an Extended Prisoner's Dilemma, or another pre-defined payoff matrix.
- Match: A Match holds Players and a Game and runs this game for a certain number of turns.
- Genetic Algorithm: Holds the code for running the GA. 
