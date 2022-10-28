from pacman_module.game import Agent
from pacman_module.game import Directions


class PacmanAgent(Agent):
    def __Utility(self, state):
        return state.getScore()

    def __Terminal_Test(self, state):
        return (state.isWin() or state.isLose())

    def __key(self, state):
        """Returns a key that uniquely identifies a Pacman game state.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A hashable key tuple.
        """
        tup = tuple([state.getPacmanPosition(),
                    state.getFood(), tuple(state.getCapsules())])

        for i in range(state.getNumAgents() - 1):
            tup = tup + (state.getGhostPosition(i + 1), )
        return tup

    def __init__(self):
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
        self.alltime_closed[curKey] = self.minimax(state)
        return self.alltime_closed[curKey]

    def minimax(self, state):
        def max_value(currentstate, depth):
            curKey = self.__key(currentstate)

            if self.__Terminal_Test(currentstate):
                return self.__Utility(currentstate)
            elif curKey in self.alltime_closed:
                return float("-inf")

            best_action = Directions.STOP
            best_score = float("-inf")

            for result, action in currentstate.generatePacmanSuccessors():
                score = min_value(result, 1, depth)
                if score > best_score:
                    best_score = score
                    best_action = action
            if depth == 0:
                return best_action

            return best_score

        def min_value(currentstate, ghostIndex, depth):
            curKey = self.__key(currentstate)

            if self.__Terminal_Test(currentstate):
                return self.__Utility(currentstate)
            elif curKey in self.alltime_closed:
                return float("inf")
            next_player = ghostIndex + 1

            if ghostIndex == currentstate.getNumAgents() - 1:
                next_player = 0

            best_score = float("inf")
            succesors = currentstate.generateGhostSuccessors(ghostIndex)
            for result, action in succesors:
                if next_player == 0:
                    score = max_value(result, depth + 1)
                else:
                    score = min_value(result, next_player, depth)
                best_score = min(best_score, float(score))

            return best_score

        maxv = max_value(state, 0)
        return maxv
