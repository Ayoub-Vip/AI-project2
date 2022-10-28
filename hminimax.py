from pacman_module.game import Agent
from pacman_module.game import Directions
import pacman_module.util as util


def heuristic_function(state):
    """ give a state instance, returns the heuristic function based on 
    the closest food distance and closest ghost distance
    state: a game state

    Returns: 
        + Score
        + manhattan distance to ghost
        - manhattan distance to nearest food

    """
    # findind closest food dist
    foodlist = state.getFood().asList()
    position = state.getPacmanPosition()
    foodLength = len(foodlist)
    closestFoodPos = foodlist[0] if foodLength != 0 else position
    closestFood= util.manhattanDistance(position, closestFoodPos)

    # findind closest food dist
    for i in range(foodLength):
        minLoc = util.manhattanDistance(position, foodlist[i])

        if minLoc< closestFood:
            closestFood = minLoc
            closestFoodPos = foodlist[i]
    score = 0
    for food in foodlist:
        dist = util.manhattanDistance(closestFoodPos, food)
        if dist!=0:
            score += 1.0/util.manhattanDistance(closestFoodPos, food)

    # findind closest ghost dist
    closestGhost = util.manhattanDistance(position, state.getGhostPosition(1))

    return state.getScore() - closestFood - score + closestGhost/2


class PacmanAgent(Agent):
    def __Utility(self, state):
        return heuristic_function(state)

    def __Terminal_Test(self, state, depth):
        return (state.isWin() or state.isLose() or depth >=self.max_depth)

    def __cut_off(self, state, depth, closed):
        curKey = self.__key(state)
        if self.__Terminal_Test(state,depth):
            return  self.__Utility(state)
        elif curKey in closed:
            return closed[curKey]
        return False

    def __key(self,state):
        """Returns a key that uniquely identifies a Pacman game state.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A hashable key tuple.
        """
        tup = tuple([state.getPacmanPosition(), state.getFood(),
             tuple(state.getCapsules())])
        for i in range(state.getNumAgents() - 1):
            tup = tup + (state.getGhostPosition(i + 1), )

        return tup

    def __init__(self):
        self.max_depth = 3
        self.alltime_closed = dict()

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.
        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        self.max_depth = 3 if util.manhattanDistance(state.getPacmanPosition(), state.getGhostPosition(1)) > 1 else 4
        curKey = self.__key(state)
        self.alltime_closed[curKey] = self.minimax(state)
        return self.alltime_closed[curKey]

       
    def minimax(self,state):
        closed =dict()

        def max_value(currentstate, depth):
            curKey = self.__key(currentstate)
            score = self.__cut_off(currentstate, depth, closed)
            if score:
                return score
            elif curKey in self.alltime_closed:
                return float("-inf")

            best_action = Directions.STOP
            best_score = float("-inf")

            for result, action in currentstate.generatePacmanSuccessors():
                score =min_value(result, 1, depth)
                if score>best_score:
                    best_score = score
                    best_action = action
            if depth == 0:
                return best_action
            closed[curKey] = best_score

            return best_score

        def min_value(currentstate, ghostIndex, depth):
            curKey = self.__key (currentstate)
            score = self.__cut_off(currentstate, depth, closed)
            if score:
                return score
            elif curKey in self.alltime_closed:
                return float("inf")
            next_player = ghostIndex + 1

            if ghostIndex == currentstate.getNumAgents() - 1:
                next_player = 0

            best_score = float("inf")
            succesors = currentstate.generateGhostSuccessors(ghostIndex)
            for result, action in succesors:
                if next_player == 0:
                    score= max_value(result, depth +1)
                else:
                    score = min_value(result, next_player, depth)
                best_score = min(best_score, float(score))

            closed[curKey] = best_score
            return best_score

        
        return max_value(state, 0)