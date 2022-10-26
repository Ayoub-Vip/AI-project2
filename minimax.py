from pacman_module.game import Agent
from pacman_module.game import Directions
import pacman_module.util as util
import sys

sys.setrecursionlimit(1500)

def Utility(currentstate):
    return currentstate.getScore()

def Terminal_Test(currentstate,depth,maxdepth):
    return (currentstate.isWin() or currentstate.isLose() or depth >= maxdepth)

def key(state):
    """Returns a key that uniquely identifies a Pacman game state.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        A hashable key tuple.
    """

    return state.getPacmanPosition(), state.getFood(), state.getGhostPosition(1)

class PacmanAgent(Agent):
    def __init__(self,args):
        self.max_depth = 4



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
        return self.minimax(state)

       
    def minimax(self,state):
        visited =dict()
        def max_value(currentstate,depth,alpha,beta):
            curKey = key (currentstate)

            if Terminal_Test(currentstate,depth,self.max_depth):
                return  Utility(currentstate)
            elif curKey in visited:
                return visited[curKey]

            best_action = Directions.STOP
            best_score = float("-inf")

            for result, action in currentstate.generatePacmanSuccessors():
                score =min_value(result,1,depth,alpha,beta)
                if score>best_score:
                    best_score = score
                    best_action = action
                #prunning
                # alpha =max(alpha,best_score)
                # if best_score >= beta:
                #     visited[curKey]=best_score
                #     return best_score
            if depth == 0:
                visited[curKey]=best_action
                return best_action
            visited[curKey]=best_score
            return best_score

        def min_value(currentstate,  ghostIndex,depth,alpha,beta):

            if Terminal_Test(currentstate,depth,self.max_depth):
                return  Utility(currentstate)
            curKey = key (currentstate)
            if curKey in visited:
                return visited[curKey]
            next_player = ghostIndex + 1

            if ghostIndex == currentstate.getNumAgents() - 1:
                next_player = 0

            best_score = float("inf")

            for result, action in currentstate.generateGhostSuccessors(ghostIndex):
                if next_player == 0:
                    score= max_value(result,depth+1,alpha,beta)
                else:
                    score= min_value(result,next_player,depth,alpha,beta)
                best_score =min(best_score,float(score))
                # prunning
                # beta = min(beta, best_score)
                # if best_score <= alpha:
                #     visited[curKey]=best_score
                #     return best_score
            visited[curKey]=best_score
            return best_score
        maxv= max_value(state,0,float("-inf"),float("inf"))
        return maxv
  


    
