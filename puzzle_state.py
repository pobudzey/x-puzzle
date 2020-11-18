import copy


class PuzzleState:
    goal_state_1 = [[1, 2, 3, 4], [5, 6, 7, 0]]
    goal_state_2 = [[1, 3, 5, 7], [2, 4, 6, 0]]
    goal_state_1_dict = {
        1: [0, 0],
        2: [0, 1],
        3: [0, 2],
        4: [0, 3],
        5: [1, 0],
        6: [1, 1],
        7: [1, 2],
    }
    goal_state_2_dict = {
        1: [0, 0],
        2: [1, 0],
        3: [0, 1],
        4: [1, 1],
        5: [0, 2],
        6: [1, 2],
        7: [0, 3],
    }

    def __init__(self, configuration, parent, cost, heuristic):
        self.configuration = configuration
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.estimate = self.get_estimate()

    def __lt__(self, state):
        return self.cost < state.cost

    def get_estimate(self):
        if not self.heuristic:
            return 0
        elif self.heuristic == "h0":
            # Heuristic #0
            if (
                self.configuration[len(self.configuration) - 1][
                    len(self.configuration[0]) - 1
                ]
                == 0
            ):
                return 0
            else:
                return 1
        elif self.heuristic == "h1":
            # Heuristic #1: Out of place tiles
            oop_tiles_g1 = oop_tiles_g2 = 0
            gs1 = [item for sublist in self.goal_state_1 for item in sublist]
            gs2 = [item for sublist in self.goal_state_2 for item in sublist]
            curr = [item for sublist in self.configuration for item in sublist]
            for x, y, z in zip(gs1, gs2, curr):
                if z != x and z != 0:
                    oop_tiles_g1 += 1
                if z != y and z != 0:
                    oop_tiles_g2 += 1
            return min(oop_tiles_g1, oop_tiles_g2)
        elif self.heuristic == "h2":
            # Heuristic #2: Manhattan distance
            sum_of_distance_1 = sum_of_distance_2 = 0
            for row in range(0, len(self.configuration)):
                for column in range(0, len(self.configuration[0])):
                    if (
                        self.configuration[row][column]
                        != self.goal_state_1[row][column]
                        and self.configuration[row][column] != 0
                    ):
                        dx = abs(
                            column
                            - self.goal_state_1_dict[self.configuration[row][column]][1]
                        )
                        dy = abs(
                            row
                            - self.goal_state_1_dict[self.configuration[row][column]][0]
                        )
                        sum_of_distance_1 = sum_of_distance_1 + dx + dy
                    if (
                        self.configuration[row][column]
                        != self.goal_state_2[row][column]
                        and self.configuration[row][column] != 0
                    ):
                        dx = abs(
                            column
                            - self.goal_state_2_dict[self.configuration[row][column]][1]
                        )
                        dy = abs(
                            row
                            - self.goal_state_2_dict[self.configuration[row][column]][0]
                        )
                        sum_of_distance_2 = sum_of_distance_2 + dx + dy
            return min(sum_of_distance_1, sum_of_distance_2)

    def find_empty_tile(self, configuration):
        for row in range(0, len(configuration)):
            for column in range(0, len(configuration[0])):
                if configuration[row][column] == 0:
                    return (row, column)

    def is_goal_state(self):
        if (
            self.configuration == self.goal_state_1
            or self.configuration == self.goal_state_2
        ):
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
            children.append(
                PuzzleState(
                    move_left_config,
                    self,
                    self.cost + 1,
                    self.heuristic,
                )
            )
        if column_0 != len(self.configuration[0]) - 1:
            move_right_config = copy.deepcopy(self.configuration)
            move_right_config[row_0][column_0] = move_right_config[row_0][column_0 + 1]
            move_right_config[row_0][column_0 + 1] = 0
            children.append(
                PuzzleState(
                    move_right_config,
                    self,
                    self.cost + 1,
                    self.heuristic,
                )
            )
        if row_0 != len(self.configuration) - 1:
            move_down_config = copy.deepcopy(self.configuration)
            move_down_config[row_0][column_0] = move_down_config[row_0 + 1][column_0]
            move_down_config[row_0 + 1][column_0] = 0
            children.append(
                PuzzleState(
                    move_down_config,
                    self,
                    self.cost + 1,
                    self.heuristic,
                )
            )
        if row_0 != 0:
            move_up_config = copy.deepcopy(self.configuration)
            move_up_config[row_0][column_0] = move_up_config[row_0 - 1][column_0]
            move_up_config[row_0 - 1][column_0] = 0
            children.append(
                PuzzleState(
                    move_up_config,
                    self,
                    self.cost + 1,
                    self.heuristic,
                )
            )
        # Wrapping and diagonal moves
        if row_0 == 0 and column_0 == 0:
            wrapping_move_config = copy.deepcopy(self.configuration)
            wrapping_move_config[row_0][column_0] = wrapping_move_config[row_0][
                len(wrapping_move_config[row_0]) - 1
            ]
            wrapping_move_config[row_0][len(wrapping_move_config[row_0]) - 1] = 0
            children.append(
                PuzzleState(
                    wrapping_move_config,
                    self,
                    self.cost + 2,
                    self.heuristic,
                )
            )
            diagonal_move_1_config = copy.deepcopy(self.configuration)
            diagonal_move_1_config[row_0][column_0] = diagonal_move_1_config[row_0 + 1][
                column_0 + 1
            ]
            diagonal_move_1_config[row_0 + 1][column_0 + 1] = 0
            children.append(
                PuzzleState(
                    diagonal_move_1_config,
                    self,
                    self.cost + 3,
                    self.heuristic,
                )
            )
            diagonal_move_2_config = copy.deepcopy(self.configuration)
            diagonal_move_2_config[row_0][column_0] = diagonal_move_2_config[
                len(diagonal_move_2_config) - 1
            ][len(diagonal_move_2_config[row_0]) - 1]
            diagonal_move_2_config[len(diagonal_move_2_config) - 1][
                len(diagonal_move_2_config[row_0]) - 1
            ] = 0
            children.append(
                PuzzleState(
                    diagonal_move_2_config,
                    self,
                    self.cost + 3,
                    self.heuristic,
                )
            )
        if row_0 == 0 and column_0 == len(self.configuration[0]) - 1:
            wrapping_move_config = copy.deepcopy(self.configuration)
            wrapping_move_config[row_0][
                len(wrapping_move_config[row_0]) - 1
            ] = wrapping_move_config[0][0]
            wrapping_move_config[0][0] = 0
            children.append(
                PuzzleState(
                    wrapping_move_config,
                    self,
                    self.cost + 2,
                    self.heuristic,
                )
            )
            diagonal_move_1_config = copy.deepcopy(self.configuration)
            diagonal_move_1_config[row_0][column_0] = diagonal_move_1_config[row_0 + 1][
                column_0 - 1
            ]
            diagonal_move_1_config[row_0 + 1][column_0 - 1] = 0
            children.append(
                PuzzleState(
                    diagonal_move_1_config,
                    self,
                    self.cost + 3,
                    self.heuristic,
                )
            )
            diagonal_move_2_config = copy.deepcopy(self.configuration)
            diagonal_move_2_config[row_0][column_0] = diagonal_move_2_config[row_0 + 1][
                0
            ]
            diagonal_move_2_config[row_0 + 1][0] = 0
            children.append(
                PuzzleState(
                    diagonal_move_2_config,
                    self,
                    self.cost + 3,
                    self.heuristic,
                )
            )
        if row_0 == len(self.configuration) - 1 and column_0 == 0:
            wrapping_move_config = copy.deepcopy(self.configuration)
            wrapping_move_config[row_0][column_0] = wrapping_move_config[row_0][
                len(wrapping_move_config[row_0]) - 1
            ]
            wrapping_move_config[row_0][len(wrapping_move_config[row_0]) - 1] = 0
            children.append(
                PuzzleState(
                    wrapping_move_config,
                    self,
                    self.cost + 2,
                    self.heuristic,
                )
            )
            diagonal_move_1_config = copy.deepcopy(self.configuration)
            diagonal_move_1_config[row_0][column_0] = diagonal_move_1_config[row_0 - 1][
                column_0 + 1
            ]
            diagonal_move_1_config[row_0 - 1][column_0 + 1] = 0
            children.append(
                PuzzleState(
                    diagonal_move_1_config,
                    self,
                    self.cost + 3,
                    self.heuristic,
                )
            )
            diagonal_move_2_config = copy.deepcopy(self.configuration)
            diagonal_move_2_config[row_0][column_0] = diagonal_move_2_config[0][
                len(diagonal_move_2_config[row_0]) - 1
            ]
            diagonal_move_2_config[0][len(diagonal_move_2_config[row_0]) - 1] = 0
            children.append(
                PuzzleState(
                    diagonal_move_2_config,
                    self,
                    self.cost + 3,
                    self.heuristic,
                )
            )
        if (
            row_0 == len(self.configuration) - 1
            and column_0 == len(self.configuration[0]) - 1
        ):
            wrapping_move_config = copy.deepcopy(self.configuration)
            wrapping_move_config[row_0][column_0] = wrapping_move_config[row_0][0]
            wrapping_move_config[row_0][0] = 0
            children.append(
                PuzzleState(
                    wrapping_move_config,
                    self,
                    self.cost + 2,
                    self.heuristic,
                )
            )
            diagonal_move_1_config = copy.deepcopy(self.configuration)
            diagonal_move_1_config[row_0][column_0] = diagonal_move_1_config[row_0 - 1][
                column_0 - 1
            ]
            diagonal_move_1_config[row_0 - 1][column_0 - 1] = 0
            children.append(
                PuzzleState(
                    diagonal_move_1_config,
                    self,
                    self.cost + 3,
                    self.heuristic,
                )
            )
            diagonal_move_2_config = copy.deepcopy(self.configuration)
            diagonal_move_2_config[row_0][column_0] = diagonal_move_2_config[0][0]
            diagonal_move_2_config[0][0] = 0
            children.append(
                PuzzleState(
                    diagonal_move_2_config,
                    self,
                    self.cost + 3,
                    self.heuristic,
                )
            )
        return children
