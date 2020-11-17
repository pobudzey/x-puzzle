import copy


class PuzzleState:
    def __init__(self, configuration, parent, cost):
        self.configuration = configuration
        self.parent = parent
        self.cost = cost

    def __lt__(self, state):
        return self.cost < state.cost

    def find_empty_tile(self, configuration):
        for row in range(0, len(configuration)):
            for column in range(0, len(configuration[0])):
                if configuration[row][column] == 0:
                    return (row, column)

    def is_goal_state(self):
        goal_state_1 = [[1, 2, 3, 4], [5, 6, 7, 0]]
        goal_state_2 = [[1, 3, 5, 7], [2, 4, 6, 0]]
        if self.configuration == goal_state_1 or self.configuration == goal_state_2:
            return True
        else:
            return False

    def reconstruct_solution_path(self):
        solution_path = []
        current_node = self
        while current_node.parent is not None:
            solution_path.insert(0, current_node)
            current_node = current_node.parent
        return solution_path

    def generate_children(self):
        children = []
        row_0, column_0 = self.find_empty_tile(self.configuration)
        # Regular moves
        if column_0 != 0:
            move_left_config = copy.deepcopy(self.configuration)
            move_left_config[row_0][column_0] = move_left_config[row_0][column_0 - 1]
            move_left_config[row_0][column_0 - 1] = 0
            children.append(PuzzleState(move_left_config, self, self.cost + 1))
        if column_0 != len(self.configuration[0]) - 1:
            move_right_config = copy.deepcopy(self.configuration)
            move_right_config[row_0][column_0] = move_right_config[row_0][column_0 + 1]
            move_right_config[row_0][column_0 + 1] = 0
            children.append(PuzzleState(move_right_config, self, self.cost + 1))
        if row_0 != len(self.configuration) - 1:
            move_down_config = copy.deepcopy(self.configuration)
            move_down_config[row_0][column_0] = move_down_config[row_0 + 1][column_0]
            move_down_config[row_0 + 1][column_0] = 0
            children.append(PuzzleState(move_down_config, self, self.cost + 1))
        if row_0 != 0:
            move_up_config = copy.deepcopy(self.configuration)
            move_up_config[row_0][column_0] = move_up_config[row_0 - 1][column_0]
            move_up_config[row_0 - 1][column_0] = 0
            children.append(PuzzleState(move_up_config, self, self.cost + 1))
        # Wrapping and diagonal moves
        if row_0 == 0 and column_0 == 0:
            wrapping_move_config = copy.deepcopy(self.configuration)
            wrapping_move_config[row_0][column_0] = wrapping_move_config[row_0][
                len(wrapping_move_config[row_0]) - 1
            ]
            wrapping_move_config[row_0][len(wrapping_move_config[row_0]) - 1] = 0
            children.append(PuzzleState(wrapping_move_config, self, self.cost + 2))
            diagonal_move_1_config = copy.deepcopy(self.configuration)
            diagonal_move_1_config[row_0][column_0] = diagonal_move_1_config[row_0 + 1][
                column_0 + 1
            ]
            diagonal_move_1_config[row_0 + 1][column_0 + 1] = 0
            children.append(PuzzleState(diagonal_move_1_config, self, self.cost + 3))
            diagonal_move_2_config = copy.deepcopy(self.configuration)
            diagonal_move_2_config[row_0][column_0] = diagonal_move_2_config[
                len(diagonal_move_2_config) - 1
            ][len(diagonal_move_2_config[row_0]) - 1]
            diagonal_move_2_config[len(diagonal_move_2_config) - 1][
                len(diagonal_move_2_config[row_0]) - 1
            ] = 0
            children.append(PuzzleState(diagonal_move_2_config, self, self.cost + 3))
        if row_0 == 0 and column_0 == len(self.configuration[0]) - 1:
            wrapping_move_config = copy.deepcopy(self.configuration)
            wrapping_move_config[row_0][
                len(wrapping_move_config[row_0]) - 1
            ] = wrapping_move_config[0][0]
            wrapping_move_config[0][0] = 0
            children.append(PuzzleState(wrapping_move_config, self, self.cost + 2))
            diagonal_move_1_config = copy.deepcopy(self.configuration)
            diagonal_move_1_config[row_0][column_0] = diagonal_move_1_config[row_0 + 1][
                column_0 - 1
            ]
            diagonal_move_1_config[row_0 + 1][column_0 - 1] = 0
            children.append(PuzzleState(diagonal_move_1_config, self, self.cost + 3))
            diagonal_move_2_config = copy.deepcopy(self.configuration)
            diagonal_move_2_config[row_0][column_0] = diagonal_move_2_config[row_0 + 1][
                0
            ]
            diagonal_move_2_config[row_0 + 1][0] = 0
            children.append(PuzzleState(diagonal_move_2_config, self, self.cost + 3))
        if row_0 == len(self.configuration) - 1 and column_0 == 0:
            wrapping_move_config = copy.deepcopy(self.configuration)
            wrapping_move_config[row_0][column_0] = wrapping_move_config[row_0][
                len(wrapping_move_config[row_0]) - 1
            ]
            wrapping_move_config[row_0][len(wrapping_move_config[row_0]) - 1] = 0
            children.append(PuzzleState(wrapping_move_config, self, self.cost + 2))
            diagonal_move_1_config = copy.deepcopy(self.configuration)
            diagonal_move_1_config[row_0][column_0] = diagonal_move_1_config[row_0 - 1][
                column_0 + 1
            ]
            diagonal_move_1_config[row_0 - 1][column_0 + 1] = 0
            children.append(PuzzleState(diagonal_move_1_config, self, self.cost + 3))
            diagonal_move_2_config = copy.deepcopy(self.configuration)
            diagonal_move_2_config[row_0][column_0] = diagonal_move_2_config[0][
                len(diagonal_move_2_config[row_0]) - 1
            ]
            diagonal_move_2_config[0][len(diagonal_move_2_config[row_0]) - 1] = 0
            children.append(PuzzleState(diagonal_move_2_config, self, self.cost + 3))
        if (
            row_0 == len(self.configuration) - 1
            and column_0 == len(self.configuration[0]) - 1
        ):
            wrapping_move_config = copy.deepcopy(self.configuration)
            wrapping_move_config[row_0][column_0] = wrapping_move_config[row_0][0]
            wrapping_move_config[row_0][0] = 0
            children.append(PuzzleState(wrapping_move_config, self, self.cost + 2))
            diagonal_move_1_config = copy.deepcopy(self.configuration)
            diagonal_move_1_config[row_0][column_0] = diagonal_move_1_config[row_0 - 1][
                column_0 - 1
            ]
            diagonal_move_1_config[row_0 - 1][column_0 - 1] = 0
            children.append(PuzzleState(diagonal_move_1_config, self, self.cost + 3))
            diagonal_move_2_config = copy.deepcopy(self.configuration)
            diagonal_move_2_config[row_0][column_0] = diagonal_move_2_config[0][0]
            diagonal_move_2_config[0][0] = 0
            children.append(PuzzleState(diagonal_move_2_config, self, self.cost + 3))
        return children
