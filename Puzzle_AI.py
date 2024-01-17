import time
import numpy as np


class PUZZLE_SOlVER:
    # [0, 1, 2], [3, 4, 5], [6, 7, 8]
    # [1, 2, 3], [4, 5, 6], [7, 8, 0]

    # [1, 2, 3], [0, 4, 6], [7, 5, 8]
    # [0, 1, 2], [3, 4, 5], [6, 7, 8]
    # [1, 2, 3], [4, 5, 6], [7, 8, 0]
    def __init__(self, start_state):
        self.GOAL_STATE = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        self.count = 0
        self.start_time = time.time()
        self.start_state = np.asarray(start_state)
        self.explored_state = []
        self.unsolvable = []
        self.solution_set = []
        if self.isSolvable(self.start_state):
            if not self.start_analysis(self.start_state):
                print("No solution found")
        else:
            print("Start state is not solvable")

    def goal_test(self, test_state):
        # check matching the goal state
        if np.array_equal(self.GOAL_STATE, test_state):
            return True
        return False

    def check(self, state):
        for explored in self.explored_state:
            if np.array_equal(explored, state):
                return True
        for s in self.unsolvable:
            if np.array_equal(s, state):
                return True
        return False

    def find_legal_actions(self, ind_blank):
        legal_action = ['U', 'D', 'L', 'R']
        i = ind_blank[0][0]
        j = ind_blank[1][0]
        if i == 0:  # up is disabled
            legal_action.remove('U')
        elif i == 2:  # down is disabled
            legal_action.remove('D')
        if j == 0:  # left is disabled
            legal_action.remove('L')
        elif j == 2:  # right is disabled
            legal_action.remove('R')
        return legal_action

    def getInvCount(self, arr):
        inv_count = 0
        empty_value = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                    inv_count += 1
        return inv_count

    def isSolvable(self, state):
        # Count inversions in given 8 puzzle
        inv_count = self.getInvCount([j for sub in state for j in sub])

        # return true if inversion count is even.
        return inv_count % 2 == 0

    def successor_function(self, state):
        # take the state , find the actions , in increasing order of the
        # number of misplaced tiles return all the successor states.
        self.explored_state.append(state)
        ind_blank = np.where(state == 0)
        legal_actions = self.find_legal_actions(ind_blank)
        successor_states = []
        h_mis_tiles = []
        for action in legal_actions:
            successor_state, mis_tiles = self.transition_function(state, action)

            if not self.check(successor_state):
                successor_states.append(successor_state)
                h_mis_tiles.append(mis_tiles)

        values = list(zip(h_mis_tiles, successor_states))
        values = sorted(values, key=lambda x: x[0])
        successor_states = [value[1] for value in values]
        # return the states in increasing order of the misplaced tiles.
        final_successor_states = np.asarray(successor_states)
        return final_successor_states

    def heuristic(self, state):
        # Number of misplaced tiles
        misplaced_tiles = np.sum(state != self.GOAL_STATE) - 1  # subtract 1 for the blank space

        # Manhattan distance
        manhattan_distance = 0
        for i in range(1, 9):  # 1-8 for 8-puzzle
            pos_state = np.where(state == i)
            pos_goal = np.where(self.GOAL_STATE == i)
            manhattan_distance += abs(pos_state[0] - pos_goal[0]) + abs(pos_state[1] - pos_goal[1])

        # Return sum of misplaced tiles and Manhattan distance
        return misplaced_tiles + manhattan_distance

    def transition_function(self, state, action):
        new_state = state.copy()

        # Find the index of the blank space (0)
        ind_blank = np.where(state == 0)
        i, j = ind_blank[0][0], ind_blank[1][0]

        # Swap the blank space with the adjacent tile based on the action
        if action == 'U':
            new_state[i, j], new_state[i - 1, j] = new_state[i - 1, j], new_state[i, j]
        elif action == 'D':
            new_state[i, j], new_state[i + 1, j] = new_state[i + 1, j], new_state[i, j]
        elif action == 'L':
            new_state[i, j], new_state[i, j - 1] = new_state[i, j - 1], new_state[i, j]
        elif action == 'R':
            new_state[i, j], new_state[i, j + 1] = new_state[i, j + 1], new_state[i, j]

        # for this new state calculate the no of misplaced tiles.
        h_tiles = self.heuristic(new_state)
        return new_state, h_tiles

    def get_solution(self):
        return self.solution_set

    def start_analysis(self, state):

        if self.goal_test(state):
            print('The game was successfully solved!')
            return True

        successor_states = self.successor_function(state)
        for s in successor_states:
            if not self.check(s) and self.isSolvable(s):
                print(f" Checking the state: {s}")
                self.count += 1
                self.solution_set.append(s)
                if self.start_analysis(s):
                    return True
                else:
                    self.solution_set.pop(-1)
                    self.unsolvable.append(s)
            else:
                self.unsolvable.append(s)

        return False
