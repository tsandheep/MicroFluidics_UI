import heapq

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.parent = None

    def __lt__(self, other):
        return self.f_score < other.f_score

def heuristic(node, goal):
    return abs(node.row - goal.row) + abs(node.col - goal.col)

def astar(start, goal, grid):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    closed_set = set()

    start_node = Node(start[0], start[1])
    goal_node = Node(goal[0], goal[1])

    start_node.g_score = 0
    start_node.f_score = heuristic(start_node, goal_node)

    heapq.heappush(open_set, start_node)

    while open_set:
        current = heapq.heappop(open_set)

        if current.row == goal_node.row and current.col == goal_node.col:
            path = []
            while current:
                path.insert(0, (current.row, current.col))
                current = current.parent
            #print("Path generated")
            return path

        closed_set.add((current.row, current.col))

        neighbors = [
            (current.row - 1, current.col),
            (current.row + 1, current.col),
            (current.row, current.col - 1),
            (current.row, current.col + 1),
        ]

        for neighbor_row, neighbor_col in neighbors:
            if (
                0 <= neighbor_row < rows
                and 0 <= neighbor_col < cols
                and grid[neighbor_row][neighbor_col] == 0
                and (neighbor_row, neighbor_col) not in closed_set
            ):
                neighbor = Node(neighbor_row, neighbor_col)
                tentative_g_score = current.g_score + 1

                if tentative_g_score < neighbor.g_score:
                    neighbor.parent = current
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = tentative_g_score + heuristic(neighbor, goal_node)

                    if neighbor not in open_set:
                        heapq.heappush(open_set, neighbor)

    return None



