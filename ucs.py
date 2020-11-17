import heapq, time
from puzzle_state import PuzzleState

start_time = time.time()

# TODO: Get puzzles from file
initial_puzzle = [[3, 0, 1, 4], [2, 6, 5, 7]]

# Initial config
initial_state = PuzzleState(initial_puzzle, None, 0)
open_list = []
heapq.heappush(open_list, (initial_state.cost, initial_state))
closed_list = []

done = False
while not done:
    if not open_list:
        print("No solution found.")
        done = True
    else:
        first = heapq.heappop(open_list)
        # Scenario warranting the if condition below:
        # We encounter a configuration that's already been visited (with a lower cost)
        # So there's no point visiting it again
        if first[1].configuration not in closed_list:
            closed_list.append(first[1].configuration)
            if first[1].is_goal_state():
                print("Goal state found!")
                done = True
            else:
                children = first[1].generate_children()
                for child in children:
                    if child.configuration not in closed_list:
                        heapq.heappush(open_list, (child.cost, child))


print("--- %s seconds ---" % (time.time() - start_time))
