import sys
from collections import deque

def read_maze(filename: str) -> list[list[str]]:

    try:
        with open(filename, 'r') as file:
            content = file.read()
        lines = [line.rstrip('\n') for line in content.splitlines() if line.strip()]
    except FileNotFoundError:
        print('File not found')
        return []
    return lines

def find_start_and_target(maze: list[list[str]]) -> tuple[int, int]:

    for row in range(len(maze)):
        for column in range(len(maze[row])):
            if maze[row][column] == 'S':
                Sposition = (row, column)
            elif maze[row][column] == 'T':
                Tposition = (row, column)
    return Sposition, Tposition

def get_neighbors(maze: list[list[str]], position: tuple[int, int]) -> list[tuple[int, int]]:

    neighbors = []
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

    for direction in directions:
        row, column = position[0] + direction[0], position[1] + direction[1]
        if 0 <= row < len(maze) and 0 <= column < len(maze[row]):
            if maze[row][column] != '#':
                neighbors.append((row, column))

    return neighbors

def bfs(maze: list[list[str]], start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
    q = deque()
    visited = set([start])
    q.append((start, [start]))

    while q:
        node, path = q.popleft()

        if node == target:
            return path

        for neighbor in get_neighbors(maze, node):
            if neighbor not in visited:
                visited.add(neighbor)
                q.append((neighbor, path + [neighbor]))

    return None


def dfs(maze: list[list[str]], start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:

    visited = {start}
    s = [(start, [start])]

    while s:
        node, path = s.pop()

        if node == target:
            return path

        for neighbor in get_neighbors(maze, node):
            if neighbor not in visited:
                visited.add(neighbor)
                s.append((neighbor, path + [neighbor]))

    return []

def print_maze_with_path(maze: list[list[str]], path: list[tuple[int, int]]) -> None:

    RED = "\033[91m"
    RESET = "\033[0m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"

    maze_copy = [list(row) for row in maze]

    for r, c in path:
        if maze_copy[r][c] not in ('S', 'T'):
            maze_copy[r][c] = f"{RED}x{RESET}"

    for r in range(len(maze_copy)):
        for c in range(len(maze_copy[r])):
            if maze_copy[r][c] == 'S':
                maze_copy[r][c] = f"{YELLOW}S{RESET}"
            elif maze_copy[r][c] == 'T':
                maze_copy[r][c] = f"{GREEN}T{RESET}"

    for row in maze_copy:
        print(''.join(row))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search_maze.py <dfs|bfs> <maze_file>")
        sys.exit(1)

    algorithm = sys.argv[1].lower()
    filename = sys.argv[2]

    maze = read_maze(filename)
    start, target = find_start_and_target(maze)

    if algorithm == 'dfs':
        path = dfs(maze, start, target)
    elif algorithm == 'bfs':
        path = bfs(maze, start, target)
    else:
        print("Unknown algorithm. Use 'dfs' or 'bfs'.")
        sys.exit(1)

    print_maze_with_path(maze, path)