from collections import deque
import heapq
import math

# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

    from collections import deque
import heapq

#step  1.2
class SearchAgent:

    def __init__(self):
        self.plan = []
        self.active_algo = 'AStar'

    def manhattan_distance(self, pos, goal):
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    
    def euclidean_distance(self, pos, goal):
        return math.sqrt(
            (pos[0] - goal[0]) ** 2 +
            (pos[1] - goal[1]) ** 2
        )
    def astar_search(
            self,
            start_pos,
            goal_pos,
            walls,
            grid_size,
            heuristic_type='manhattan'
        ):
            frontier = []
            reached_states = set()

            # Calculate heuristic for starting position
            if heuristic_type == 'euclidean':
                h_cost = self.euclidean_distance(start_pos, goal_pos)
            else:
                h_cost = self.manhattan_distance(start_pos, goal_pos)

            g_cost = 0
            f_cost = g_cost + h_cost

            # (f_cost, g_cost, current_pos, path_taken)
            heapq.heappush(
                frontier,
                (f_cost, g_cost, start_pos, [start_pos])
            )

            while frontier:

                f_cost, g_cost, current_pos, path_taken = heapq.heappop(frontier)

                # Goal reached
                if current_pos == goal_pos:
                    return path_taken

                if current_pos in reached_states:
                    continue

                reached_states.add(current_pos)

                # Get valid neighbors
                for neighbor in self.get_neighbors(
                    current_pos,
                    grid_size,
                    walls
                ):

                    if neighbor not in reached_states:

                        # g(n)
                        new_g = g_cost + 1

                        # h(n)
                        if heuristic_type == 'euclidean':
                            new_h = self.euclidean_distance(
                                neighbor,
                                goal_pos
                            )
                        else:
                            new_h = self.manhattan_distance(
                                neighbor,
                                goal_pos
                            )

                        # f(n) = g(n) + h(n)
                        new_f = new_g + new_h

                        heapq.heappush(
                            frontier,
                            (
                                new_f,
                                new_g,
                                neighbor,
                                path_taken + [neighbor]
                            )
                        )

            return None

    def get_neighbors(self, position, grid_size, walls):
        x, y = position
        width, height = grid_size

        possible_moves = [
            (x, y + 1),  # Up
            (x, y - 1),  # Down
            (x - 1, y),  # Left
            (x + 1, y)   # Right
        ]

        valid_neighbors = []

        for nx, ny in possible_moves:
            if (
                0 <= nx < width
                and 0 <= ny < height
                and (nx, ny) not in walls
            ):
                valid_neighbors.append((nx, ny))

        return valid_neighbors

     

    # ---------------- BFS ----------------
    def bfs_search(self, start, goal, grid_size, walls):

        frontier = deque()
        frontier.append((start, [start]))

        reached = set()
        reached.add(start)

        while frontier:

            current, path = frontier.popleft()

            if current == goal:
                return path

            for neighbor in self.get_neighbors(current, grid_size, walls):

                if neighbor not in reached:
                    reached.add(neighbor)
                    frontier.append((neighbor, path + [neighbor]))

        return None


    # ---------------- DFS ----------------
    def dfs_search(self, start, goal, grid_size, walls):

        frontier = []
        frontier.append((start, [start]))

        reached = set()
        reached.add(start)

        while frontier:

            current, path = frontier.pop()

            if current == goal:
                return path

            for neighbor in self.get_neighbors(current, grid_size, walls):

                if neighbor not in reached:
                    reached.add(neighbor)
                    frontier.append((neighbor, path + [neighbor]))

        return None


    # ---------------- UCS ----------------
    def ucs_search(self, start, goal, grid_size, walls):

        frontier = []
        heapq.heappush(frontier, (0, start, [start]))

        reached = set()

        while frontier:

            cost, current, path = heapq.heappop(frontier)

            if current in reached:
                continue

            reached.add(current)

            if current == goal:
                return path

            for neighbor in self.get_neighbors(current, grid_size, walls):

                if neighbor not in reached:

                    new_cost = cost + 1

                    heapq.heappush(
                        frontier,
                        (new_cost, neighbor, path + [neighbor])
                    )

        return None
    def sense_and_act(self, percept):

        if not self.plan:

            start = tuple(percept['agent_pos'])
            foods = percept['all_food']

            if not foods:
                return None

            goal = min(
                foods,
                key=lambda food: abs(food[0] - start[0]) + abs(food[1] - start[1])
            )

            grid_size = percept['grid_size']
            walls = set(percept['walls'])

            if self.active_algo == 'BFS':
                path = self.bfs_search(start, goal, grid_size, walls)

            elif self.active_algo == 'DFS':
                path = self.dfs_search(start, goal, grid_size, walls)

            elif self.active_algo == 'UCS':
                path = self.ucs_search(start, goal, grid_size, walls)

            elif self.active_algo == 'AStar':
                    path = self.astar_search(
                        start,
                        goal,
                        walls,
                        grid_size,
                        heuristic_type='manhattan'
                    )

            if path:
                self.plan = self.path_to_actions(path)

        if self.plan:
            return self.plan.pop(0)

        return None

    def path_to_actions(self, path):
        actions = []

        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            if x2 > x1:
                actions.append("Right")
            elif x2 < x1:
                actions.append("Left")
            elif y2 > y1:
                actions.append("Up")
            elif y2 < y1:
                actions.append("Down")

        return actions

if __name__ == "__main__":
    agent = SearchAgent()

    start = (0, 0)
    goal = (3, 4)

    print("Manhattan:", agent.manhattan_distance(start, goal))
    print("Euclidean:", agent.euclidean_distance(start, goal))