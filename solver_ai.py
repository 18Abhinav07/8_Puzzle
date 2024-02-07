import copy
import heapq
from itertools import count

import numpy as np


class State:
    def __init__(self, list_of_tiles, parent=None):
        self.board = np.array(list_of_tiles)
        self.parent = parent


class Solver:
    def __init__(self, start_state, goal_state, width):
        self.start_state = start_state
        self.goal_state = goal_state
        self.width = width
        self.path = []
        self.itr = 0
        self.counter = count()
        self.explored = set()

    def check_solvability(self, state):
        cur_inversions = self.inversions(state)
        goal_Inversions = self.inversions(self.goal_state)

        if self.width % 2 == 0:
            goalZeroRowIndex = np.where(state.board == 0)[0][0]
            startZeroRowIndex = np.where(state.board == 0)[0][0]
            return (goal_Inversions % 2) == ((cur_inversions + goalZeroRowIndex + startZeroRowIndex) % 2)
        else:
            return (cur_inversions % 2) == (goal_Inversions % 2)

    def inversions(self, state):
        inv_count = 0
        empty_value = 0
        arr = [j for row in state.board for j in row]
        for i in range(0, (self.width ** 2)):
            for j in range(i + 1, 9):
                if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                    inv_count += 1
        return inv_count

    def get_next_states(self, state):
        next_states = []

        empty_row, empty_col = np.where(state.board == 0)
        empty_row, empty_col = empty_row[0], empty_col[0]

        # Define possible moves (up, down, left, right)
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for move in moves:
            new_row, new_col = empty_row + move[0], empty_col + move[1]

            if 0 <= new_row < self.width and 0 <= new_col < self.width:
                new_board = copy.deepcopy(state.board)
                new_board[empty_row, empty_col], new_board[new_row, new_col] = (
                    new_board[new_row, new_col],
                    new_board[empty_row, empty_col],
                )
                # print(new_board)
                new_state = State(new_board, parent=state)
                # print(self.heuristic(new_state))
                next_states.append(new_state)
        return next_states

    def heuristic(self, state):
        # Number of misplaced tiles
        misplaced_tiles = np.sum(state.board != self.goal_state) - 1  # subtract 1 for the blank space

        # Manhattan distance
        manhattan_distance = 0
        for i in range(1, (self.width ** 2)):  # 1-8 for 8-puzzle
            pos_state = np.where(state.board == i)
            pos_goal = np.where(self.goal_state.board == i)
            manhattan_distance += abs(pos_state[0] - pos_goal[0]) + abs(pos_state[1] - pos_goal[1])

        # Return sum of misplaced tiles and Manhattan distance
        return misplaced_tiles + manhattan_distance

    def solver(self):

        priority_queue = []
        heapq.heappush(priority_queue, (self.heuristic(self.start_state), next(self.counter), self.start_state))

        while priority_queue:
            heurisitc_val, _, current_state = heapq.heappop(priority_queue)
            self.itr += 1

            if np.array_equal(current_state.board, self.goal_state.board):
                self.construct_path(current_state)
                return True

            self.explored.add(tuple(current_state.board.flatten()))

            next_states = self.get_next_states(current_state)
            for next_state in next_states:
                if tuple(next_state.board.flatten()) not in self.explored:
                    heapq.heappush(priority_queue, (self.heuristic(next_state), next(self.counter), next_state))

        return None  # No solution found

    def construct_path(self, goal_state):
        self.path = [goal_state.board]
        current_state = goal_state.parent

        while current_state:
            self.path.append(current_state.board)
            current_state = current_state.parent

        return self.path[::-1]
