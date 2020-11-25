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
    initial_state = PuzzleState(puzzle, None, 0, None)
    open_list = []
    heapq.heappush(open_list, (initial_state.cost, initial_state))
    closed_list = []
    start_time = time.clock()
    done = False
    no_solution_found = False
    while not done:
        if time.clock() - start_time > 60:
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
                            heapq.heappush(open_list, (child.cost, child))
    execution_time = time.clock() - start_time

    path_to_output = Path.cwd().parent / "output"
    path_to_output.mkdir(parents=True, exist_ok=True)
    with open(path_to_output / f"{count}_ucs_solution.txt", "w") as f:
        if no_solution_found:
            f.write("No solution found.")
        else:
            for step in solution_path:
                step = [item for sublist in step.configuration for item in sublist]
                step = [str(x) for x in step]
                step = " ".join(step)
                f.write(step + "\n")
            f.write(str(solution_path_cost) + " " + str(execution_time))
