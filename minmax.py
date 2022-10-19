from pacman_module.game import Agent
from pacman_module.game import Directions
import pacman_module.util as util
import sys

sys.setrecursionlimit(1500)

class PacmanAgent(Agent):
    PACMAN = 0
    def __init__(self,args):
        self.depth = 5000



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
        def Utility(currentstate):
            return currentstate.getScore()
        def Terminal_Test(currentstate):
            return currentstate.isWin() or currentstate.isLose()
        def Actions(currentstate,player):
            return currentstate.getLegalActions(player)
        def Result (currentstate,player,action):
            return currentstate.generateSuccessor(player, action)
        def key(currentstate):
            return currentstate.getPacmanPosition(), currentstate.getFood(), currentstate.getGhostPosition(1)
    
        def max_value(currentstate,depth,alpha,beta,visited):
            current = key(currentstate)

            if Terminal_Test(currentstate):
                return  Utility(currentstate)
            elif current in visited:
                return visited[current]
            best_action = Directions.STOP
            best_score = float("-inf")
            visited[current] = best_score

            for action in Actions(currentstate,0):
                score =min_value(Result(currentstate,0,action),1,depth,alpha,beta,visited)
                if score>best_score:
                    best_score = score
                    best_action = action
                alpha =max(alpha,best_score)
                if best_score >= beta:
                    return best_score
            visited[current] = best_score

            if depth == 0:
                return best_action
            return best_score

        def min_value(currentstate,  ghost,depth,alpha,beta,visited):
            current = key(currentstate)

            if Terminal_Test(currentstate):
                return  Utility(currentstate)
            elif current in visited:
                return visited[current]
            next_player = ghost + 1
            if ghost == state.getNumAgents() - 1:
                next_player = 0

            best_score = float("inf")
            visited[current] = best_score

            for action in Actions(currentstate,ghost):
                result =Result(currentstate,ghost,action)
                if next_player == 0:
                    # if (depth == self.depth - 1):
                    #     score = currentstate.getScore()
                    # else :
                    #     depth+=1
                        score= max_value(result,depth+1,alpha,beta,visited)
                else:
                    score= min_value(result,next_player,depth,alpha,beta,visited)
                best_score =min(best_score,float(score))
                beta = min(beta, best_score)
                if best_score <= alpha:
                    return best_score
            visited[current] = best_score
            return best_score

        maxv= max_value(state,0,float("-inf"),float("inf"),dict())
        return maxv


    
