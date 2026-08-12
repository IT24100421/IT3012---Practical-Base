from collections import deque
import heapq

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
        self.active_algo = 'DFS'

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