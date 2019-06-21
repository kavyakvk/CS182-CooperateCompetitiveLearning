# CoperativeCompetitiveLearning
Cooperative and Competitive Learning Agents in games with Non Pareto Optimal Nash Equilibria

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
