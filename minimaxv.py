# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
import numpy as np


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
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.depth = np.inf()
        self.a = list()

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


        def minimax(state):
            action = dict()
                for s, a in state.generatePacmanSuccessors():
                    action[a] = list()

            if Terminal_Test(state):
                return Utility(state)

            def Max_Value(Pstate, depth, firstAction):
                if Terminal_Test(Pstate):
                    return Utility(Pstate)

                v = -np.inf()
                for s, act in Pstate.generatePacmanSuccessors():
                    action[firstAction] = max(Min_Value(s, depth - 1, action), a)

            def Min_Value(Gstate, depth, FisrtAction):
                if Terminal_Test(Pstate):
                    return Utility(Pstate)

                v = np.inf()
                for s, act in Gstate.generateGhostSuccessors():
                     = min(Max_Value(s, depth - 1, action), action[a])


        return action.[minimax(state)]  #Directions.STOP
