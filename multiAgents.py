# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import datetime
import math
from random import choice

from game import Agent

# if you only have one move you should return it !!!!!!!!!!
class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
      python pacman.py -p MinimaxAgent -a depth=2
    """

    def minimax(self, gameState, depth, player, num_players): # is self a gameState or not?

        if (depth == 0 or gameState.isWin() or gameState.isLose()): # if state n is TERMINAL
            return [self.evaluationFunction(gameState), Directions.RIGHT]  # terminal states utility

        if player == 0: # pacman is the maximizer
            best_val = float("-infinity")
            best_action = Directions.STOP
            legal_actions = gameState.getLegalActions(player)

            for action in legal_actions:
                child = gameState.generateSuccessor(player, action) # generates children
                val, act = self.minimax(child, depth, (player + 1) % num_players, num_players)
                if val > best_val:
                    best_val = val
                    best_action = action
            return [best_val, best_action]

        else: # ghosts
            best_val = float("infinity")
            best_action = Directions.STOP
            for action in gameState.getLegalActions(player):
                child = gameState.generateSuccessor(player, action) # generates child
                if (player + 1) % num_players == 0:
                    val, act = self.minimax(child, depth - 1, (player + 1) % num_players, num_players)
                else:
                    val, act = self.minimax(child, depth, (player + 1) % num_players, num_players)

                if val < best_val:
                    best_val = val
                    best_action = action
            return [best_val, best_action]

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game: pacman + num ghosts
        """
        "*** YOUR CODE HERE ***"
        num_agents = gameState.getNumAgents()  # gets the number of agents
        best_val, best_action = self.minimax(gameState, self.depth, 0, num_agents)
        return best_action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def minimax_w_alphabeta(self, gameState, depth, alpha, beta, player, num_players): # is self a gameState or not?
        if (depth == 0 or gameState.isWin() or gameState.isLose()): # if state n is TERMINAL
            return [self.evaluationFunction(gameState), Directions.RIGHT]  # terminal states utility

        if player == 0: # pacman is the maximizer
            best_val = float("-infinity")
            best_action = Directions.STOP
            legal_actions = gameState.getLegalActions(player)

            for action in legal_actions:
                child = gameState.generateSuccessor(player, action) # generates children
                alpha_prime, act = self.minimax_w_alphabeta(child, depth, alpha, beta, (player + 1) % num_players, num_players)
                if alpha_prime > alpha:
                    alpha = alpha_prime
                    best_action = action
                if beta <= alpha:
                    break
            return [alpha, best_action]

        else: # ghosts
            best_val = float("infinity")
            best_action = Directions.STOP
            for action in gameState.getLegalActions(player):
                child = gameState.generateSuccessor(player, action) # generates child
                if (player + 1) % num_players == 0:
                    beta_prime, act = self.minimax_w_alphabeta(child, depth - 1, alpha, beta, (player + 1) % num_players, num_players)
                else:
                    beta_prime, act = self.minimax_w_alphabeta(child, depth, alpha, beta, (player + 1) % num_players, num_players)
                if beta_prime < beta:
                    beta = beta_prime
                    best_action = action
                if beta <= alpha:
                    break
            return [beta, best_action]

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        num_agents = gameState.getNumAgents()  # gets the number of agents
        best_val, best_action = self.minimax_w_alphabeta(gameState, self.depth, float("-infinity"), float("infinity"), 0, num_agents)
        return best_action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent): #take average of children node
    """
      Your expectimax agent (question 4)
    """
    # check if there are no more legal actions as terminal nodes
    def expectimax(self, gameState, depth, player, num_players): # is self a gameState or not?

        if (depth == 0 or gameState.isWin() or gameState.isLose()): # if state n is TERMINAL
            return [self.evaluationFunction(gameState), Directions.RIGHT]  # terminal states utility

        if player == 0: # pacman is the maximizer
            best_val = float("-infinity")
            best_action = Directions.STOP
            legal_actions = gameState.getLegalActions(player)

            for action in legal_actions:
                child = gameState.generateSuccessor(player, action) # generates children
                val, act = self.expectimax(child, depth, (player + 1) % num_players, num_players)
                if val > best_val:
                    best_val = val
                    best_action = action
            return [best_val, best_action]

        else: # ghosts (minimizer)
            total = 0
            actions = gameState.getLegalActions(player)
            for action in actions:
                child = gameState.generateSuccessor(player, action) # generates child
                if (player + 1) % num_players == 0:
                    val, act = self.expectimax(child, depth - 1, (player + 1) % num_players, num_players)
                else:
                    val, act = self.expectimax(child, depth, (player + 1) % num_players, num_players)
                total += val
            return [total/float(len(actions)), Directions.STOP] # don't think the action matters in minimizing agent as only the maximizers makes the move

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        num_agents = gameState.getNumAgents()  # gets the number of agents
        best_val, best_action = self.expectimax(gameState, self.depth, 0, num_agents)
        return best_action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    num_agents = gameState.getNumAgents()  # gets the number of agents
    best_val, best_action = self.minimax_w_alphabeta(gameState, self.depth, float("-infinity"), float("infinity"), 0,
                                                     num_agents)
    return best_action
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

# add the function scoreEvaluationFunction to multiAgents.py
def scoreEvaluationFunction(currentGameState):
   """
     This default evaluation function just returns the score of the state.
     The score is the same one displayed in the Pacman GUI.

     This evaluation function is meant for use with adversarial search agents
   """
   return currentGameState.getScore()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (to help improve your UCT MCTS).
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()