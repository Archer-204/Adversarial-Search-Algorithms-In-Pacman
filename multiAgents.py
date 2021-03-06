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

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = min(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = currentGameState.getFood().asList()
        newPosList = list(newPos)

        for ghostState in newGhostStates:
            if ghostState.getPosition() == tuple(newPosList) and ghostState.scaredTimer is 0:
                return float("inf") 

        minCost = min([(util.manhattanDistance(newPosList, food)) for food in foodList])
        return (minCost)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

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
    """

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
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        curDep = self.depth
        curAgent = 0
        act, v = self.value(gameState, curDep, curAgent)
        return act


    def value(self, gameState, curDep, curAgent): 
        if curAgent >= gameState.getNumAgents():
            curAgent = 0
            curDep -= 1

        if curDep == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)


        if curAgent == 0:
            return self.max_value(gameState, curDep, curAgent)
        else:
            return self.min_value(gameState, curDep, curAgent)

    def min_value(self, gameState, curDep, curAgent):
        v =  float("inf")
        act = ""
        for action in gameState.getLegalActions(curAgent):
            val = self.value(gameState.generateSuccessor(curAgent, action), curDep, curAgent + 1)
            if type(val) is tuple:
                val = val[1] 
            if val < v:
                v = val
                avt = action
   
        return (act, v)

    def max_value(self, gameState, curDep, curAgent):
        v = -1*float("inf")
        act = ""
        for action in gameState.getLegalActions(curAgent):
            val = self.value(gameState.generateSuccessor(curAgent, action), curDep, curAgent + 1)
            if type(val) is tuple:
                val = val[1] 
            if val > v:
                v = val
                act = action

        return (act, v)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        curDep = self.depth
        curAgent = 0
        alpha = -1*float("inf")
        beta = float("inf")
        act, v = self.value(gameState, curAgent, curDep, alpha, beta)
        return act

    def value(self, gameState, curAgent, curDep, alpha, beta): 
        if curAgent >= gameState.getNumAgents():
            curAgent = 0
            curDep -= 1

        if curDep == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if curAgent == 0:
            return self.max_value(gameState, curAgent, curDep, alpha, beta)
        else:
            return self.min_value(gameState, curAgent, curDep, alpha, beta)
        
    def min_value(self, gameState, curAgent, curDep, alpha, beta):
        v = float("inf")
        act = ""
        for action in gameState.getLegalActions(curAgent): 
            val = self.value(gameState.generateSuccessor(curAgent, action), curAgent + 1, curDep, alpha, beta)
            if type(val) is tuple:
                val = val[1] 
            if val < v:
                v = val
                act = action 
            if v < alpha:
                return (act, v)
            beta = min(beta, v)
        return (act, v)

    def max_value(self, gameState, curAgent, curDep, alpha, beta):
        v = -1*float("inf")
        act = ""
        for action in gameState.getLegalActions(curAgent):
            val = self.value(gameState.generateSuccessor(curAgent, action), curAgent + 1, curDep, alpha, beta)
            if type(val) is tuple:
                val = val[1] 
            if val > v:
                v = val
                act = action 
            if v > beta:
                return (act, v)
            alpha = max(alpha, v)
        return (act, v)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        curDep = self.depth
        curAgent = 0
        act, v = self.value(gameState, curAgent, curDep)
        return act
        util.raiseNotDefined()

    def value(self, gameState, curAgent, curDep): 
        if curAgent >= gameState.getNumAgents():
            curAgent = 0
            curDep -= 1

        if curDep == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if curAgent == 0:
            return self.max_value(gameState, curAgent, curDep)
        else:
            return self.exp_value(gameState, curAgent, curDep)
        
    def exp_value(self, gameState, curAgent, curDep):
        v = 0
        act = ""
        p = 1.0/len(gameState.getLegalActions(curAgent))
        for action in gameState.getLegalActions(curAgent): 
            val = self.value(gameState.generateSuccessor(curAgent, action), curAgent + 1, curDep)
            if type(val) is tuple:
                val = val[1] 
            v += val * p
            act = action
        return tuple([act, v])

    def max_value(self, gameState, curAgent, curDep):
        v = -1*float("inf")
        act = ""
        for action in gameState.getLegalActions(curAgent):
            val = self.value(gameState.generateSuccessor(curAgent, action), curAgent + 1, curDep)
            if type(val) is tuple:
                val = val[1] 
            if val > v:
                v = val
                act = action  
        return (act, v)
 

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction