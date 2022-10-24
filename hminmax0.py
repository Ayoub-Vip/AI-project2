from pacman_module.game import Agent
from pacman_module.game import Directions
import pacman_module.util as util

def Utility(currentstate):
    return heuristic_function(currentstate)
def Terminal_Test(currentstate,depth):
    print("depth:"+str(depth))
    return (currentstate.isWin() or currentstate.isLose() or depth >=10)
def Actions(currentstate,player):
    return currentstate.getLegalActions(player)
def Result (currentstate,player,action):
    return currentstate.generateSuccessor(player, action)
def heuristic_function(state):
    """ give a state instance, returns the heuristic function based on 
    remaining number of food in addition to the average distances between sequence 
    of food
    
    Arguments: 
    state: a game state

    Returns: 
        heuritic function
    """
    foodlist = state.getFood().asList()
    position = state.getPacmanPosition()
    minLoc=0
    maxLoc=0
    closest=[]
    farest=[]
    far =0
    for i in range(len(foodlist)):
        man =util.manhattanDistance(position, foodlist[i])
        if i==0:
                minLoc=man
                farest = foodlist[i]
                closest = foodlist[i]

        if man < minLoc:
                minLoc = man
                closest = foodlist[i]
        if man > maxLoc:
                maxLoc=man
                farest = foodlist[i]
        
        if len(closest)>0:
            far=util.manhattanDistance(closest, farest)

    return state.getScore()-minLoc-far+util.manhattanDistance(position, state.getGhostPosition(1))*(state.isWin() is False)/2

class PacmanAgent(Agent):
    PACMAN = 0
    def __init__(self,args):
        self.depth = 2

    def max_value(self,currentstate,depth,alpha,beta,visited):

        if Terminal_Test(currentstate,depth):
            return  Utility(currentstate)
        best_action = Directions.STOP
        best_score = float("-inf")

        for action in Actions(currentstate,0):
            score =self.min_value(Result(currentstate,0,action),1,depth,alpha,beta,visited)
            if score>best_score:
                best_score = score
                best_action = action
            alpha =max(alpha,best_score)
            if best_score >= beta:
                return best_score

        if depth == 0:
            return best_action
        return best_score

    def min_value(self,currentstate,  ghost,depth,alpha,beta,visited):
        # current = key(currentstate)

        if Terminal_Test(currentstate,depth):
            return  Utility(currentstate)

        next_player = ghost + 1

        if ghost == currentstate.getNumAgents() - 1:
            next_player = 0

        best_score = float("inf")

        for action in Actions(currentstate,ghost):
            result =Result(currentstate,ghost,action)
            if next_player == 0:
                depth+=1
                score= self.max_value(result,depth+1,alpha,beta,visited)
            else:
                score= self.min_value(result,next_player,depth,alpha,beta,visited)
            best_score =min(best_score,float(score))
            beta = min(beta, best_score)
            if best_score <= alpha:
                return best_score
        return best_score

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
        return self.min_max(state)

       
    def min_max(self,state):
        maxv= self.max_value(state,0,float("-inf"),float("inf"),dict())
        return maxv
  


    
