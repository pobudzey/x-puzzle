import heapq, time
from puzzle_state import PuzzleState
from pathlib import Path

path_to_input = Path.cwd().parent / "input" / "samplePuzzles.txt"
if path_to_input.exists():
    with open(path_to_input) as f:
        puzzles = f.readlines()
puzzles = [x.strip() for x in puzzles]
puzzles = [[int(s) for s in puzzle.split(" ")] for puzzle in puzzles]
puzzles = [
    [puzzle[: len(puzzle) // 2], puzzle[len(puzzle) // 2 :]] for puzzle in puzzles
]


for count, puzzle in enumerate(puzzles):
    # To run the algorithm with the second heuristic, do the following:
    # (1) Change h1 to h2 on line 21
    # (2) Change h1 to h2 on line 54
    # (2) Change h1 to h2 on line 56
    initial_state = PuzzleState(puzzle, None, 0, "h1")
    open_list = []
    heapq.heappush(
        open_list, (initial_state.cost + initial_state.estimate, initial_state)
    )
    closed_list = []
    start_time = time.clock()
    done = False
    no_solution_found = False
    while not done:
        if time.clock() - start_time > 120:
            done = True
            no_solution_found = True
        if not open_list:
            print("No solution found.")
            done = True
        else:
            first = heapq.heappop(open_list)
            if first[1].configuration not in closed_list:
                closed_list.append(first[1].configuration)
                if first[1].is_goal_state():
                    solution_path = first[1].reconstruct_solution_path()
                    solution_path_cost = first[1].cost
                    done = True
                else:
                    children = first[1].generate_children()
                    for child in children:
                        if child.configuration not in closed_list:
                            heapq.heappush(
                                open_list, (child.cost + child.estimate, child)
                            )
    execution_time = time.clock() - start_time

    path_to_output = Path.cwd().parent / "output" / "astar-h1"
    path_to_output.mkdir(parents=True, exist_ok=True)
    with open(path_to_output / f"{count}_astar-h1_solution.txt", "w") as f:
        if no_solution_found:
            f.write("No solution found.")
        else:
            for step in solution_path:
                step = [item for sublist in step.configuration for item in sublist]
                step = [str(x) for x in step]
                step = " ".join(step)
                f.write(step + "\n")
            f.write(str(solution_path_cost) + " " + str(execution_time))