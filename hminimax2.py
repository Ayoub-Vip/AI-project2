from pacman_module.game import Agent
from pacman_module.game import Directions
import pacman_module.util as util

def heuristic_function(state):
    """ give a state instance, returns the heuristic function based on 
    the closest food distance and closest ghost distance
    state: a game state

    Returns: 
        result
    """
    # findind closest food dist
    foodlist = state.getFood().asList()
    position = state.getPacmanPosition()
    # closestFood=-1

    # for i in range(len(foodlist)):
    #     minLoc =util.manhattanDistance(position, foodlist[i])
    #     if i==0:
    #         closestFood=minLoc
    #     else:
    #         closestFood=min(minLoc,closestFood)
    score = 0
    current_food = position
    for food in foodlist:
        #return the nearest_food using the below line.
        nearest_food = min(foodlist, key=lambda x: util.manhattanDistance(x, current_food))
        score += 1.0/util.manhattanDistance(nearest_food, current_food)
        foodlist.remove(nearest_food)
        current_food = nearest_food
    # findind closest ghost dist
    closestGhost=1
    for i in range(state.getNumAgents()-1):
        minLoc =util.manhattanDistance(position, state.getGhostPosition(i+1))
        if i==0:
            closestGhost=minLoc
        else :
            closestGhost=min(minLoc,closestGhost)
 
    return state.getScore() +score + closestGhost/2


class PacmanAgent(Agent):
    def __Utility(self,state):
        return heuristic_function(state)
    def __Terminal_Test(self,state,depth):
        return (state.isWin() or state.isLose() or depth >=self.max_depth)
    def __cut_off(self,state,depth,closed):
        curKey=self.__key(state)
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
        tup = tuple([state.getPacmanPosition(), state.getFood(), tuple(state.getCapsules())])
        for i in range(state.getNumAgents()-1):
            tup = tup+ (state.getGhostPosition(i+1),)
        return tup

    def __init__(self,args):
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
        curKey = self.__key(state)
        self.alltime_closed[curKey]=self.minimax(state)
        return self.alltime_closed[curKey]

       
    def minimax(self,state):
        closed =dict()
        def max_value(currentstate,depth):
            curKey = self.__key(currentstate)
            score = self.__cut_off(currentstate,depth,closed)
            if score:
                return score
            elif curKey in self.alltime_closed:
                return float("-inf")

            best_action = Directions.STOP
            best_score = float("-inf")

            for result, action in currentstate.generatePacmanSuccessors():
                score =min_value(result,1,depth)
                if score>best_score:
                    best_score = score
                    best_action = action
            if depth == 0:
                return best_action
            closed[curKey]=best_score

            return best_score

        def min_value(currentstate,  ghostIndex,depth):
            curKey = self.__key (currentstate)

            if self.__Terminal_Test(currentstate,depth):
                return  self.__Utility(currentstate)
            elif curKey in closed:
                return closed[curKey]
            elif curKey in self.alltime_closed:
                return float("inf")
            next_player = ghostIndex + 1

            if ghostIndex == currentstate.getNumAgents() - 1:
                next_player = 0

            best_score = float("inf")

            for result, action in currentstate.generateGhostSuccessors(ghostIndex):
                if next_player == 0:
                    score= max_value(result,depth+1)
                else:
                    score= min_value(result,next_player,depth)
                best_score =min(best_score,float(score))

            closed[curKey]=best_score
            return best_score
        maxv= max_value(state,0)
        return maxv
