import sys


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def build_corrupted_tiles(text: str) -> list[tuple[int, int]]:
    coordinate_list = text.split("\n")

    coordinates = []
    for co in coordinate_list:
        val1, val2 = co.split(",")
        coordinates.append((int(val1), int(val2)))

    return coordinates


class Direction:
    EAST = (1, 0)
    NORTH = (0, -1)
    WEST = (-1, 0)
    SOUTH = (0, 1)


def get_neighbors(pos: tuple[int, int], maze: list[list[str]]) -> list[tuple[int, int]]:
    up = (pos[0], pos[1] - 1)
    down = (pos[0], pos[1] + 1)
    left = (pos[0] - 1, pos[1])
    right = (pos[0] + 1, pos[1])

    directions = [up, down, left, right]
    valid_directions = []
    for dir in directions:
        if 0 <= dir[0] < len(maze[0]) and 0 <= dir[1] < len(maze) and maze[dir[0]][dir[1]] != '#':
            valid_directions.append(dir)

    return valid_directions


def dijkstra(
        maze: list[list[str]]
) -> dict[tuple[int, int], int]:
    width = len(maze[0])
    height = len(maze)
    distance_matrix = {}
    visited_matrix = {}
    previous_matrix = {}

    for x in range(width):
        for y in range(height):
            if 0 <= x < width and 0 <= y < height and maze[x][y] != '#':
                distance_matrix[(x, y)] = sys.maxsize
                visited_matrix[(x, y)] = False
                previous_matrix[(x, y)] = (-1, -1)

    distance_matrix[(0, 0)] = 0
    distance_matrix[(0, 0)] = 0

    previous_matrix[(0, 0)] = (0, 0)

    to_analyze = [(0, 0)]
    while len(to_analyze) > 0:
        pos = to_analyze.pop(0)
        neighbors = get_neighbors(pos, maze)
        neighbors.sort(key=lambda n: distance_matrix[n])
        for neighbor in neighbors:
            if visited_matrix[neighbor]:
                continue
            if neighbor not in to_analyze and maze[neighbor[1]][neighbor[0]] != 'E':
                to_analyze.append(neighbor)
            actual_distance = distance_matrix[pos] + 1
            if actual_distance < distance_matrix[neighbor]:
                distance_matrix[neighbor] = actual_distance
                previous_matrix[neighbor] = pos
        visited_matrix[pos] = True
        to_analyze.sort(key=lambda n: distance_matrix[n])

    return distance_matrix


def get_shortest_path(text: str, dim: int, num_cor_tiles: int) -> int:
    corrupted_tiles = build_corrupted_tiles(text)[:num_cor_tiles]

    maze = [['.' if (x, y) not in corrupted_tiles else '#' for x in range(dim)] for y in range(dim)]
    maze[-1][-1] = 'E'

    for x in range(dim):
        for y in range(dim):
            print(maze[y][x], end="")
        print()

    dist = dijkstra(maze)

    min_score = dist[(dim - 1, dim - 1)]
    return min_score


def get_shortest_path_v2(text: str, dim: int, num_cor_tiles: int) -> tuple[int, int]:
    corrupted_tiles = build_corrupted_tiles(text)

    maze = [['.' if (x, y) not in corrupted_tiles[:num_cor_tiles] else '#' for x in range(dim)] for y in range(dim)]
    maze[-1][-1] = 'E'

    is_possible = True
    i = 0
    new_corrupted_tile = corrupted_tiles[num_cor_tiles + i]
    while is_possible:
        new_corrupted_tile = corrupted_tiles[num_cor_tiles + i]
        maze[new_corrupted_tile[1]][new_corrupted_tile[0]] = '#'
        dist = dijkstra(maze)

        min_score = dist[(dim - 1, dim - 1)]
        if min_score == sys.maxsize:
            is_possible = False

        i += 1

    return new_corrupted_tile


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    dim = 7
    num_corrupted_tiles = 12
    print(get_shortest_path(input_text, dim, num_corrupted_tiles))

    # Real input
    input_text = get_input_from_file("input.txt")
    dim = 71
    num_corrupted_tiles = 1024
    print(get_shortest_path(input_text, dim, num_corrupted_tiles))

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    dim = 7
    num_corrupted_tiles = 12
    print(get_shortest_path_v2(input_text, dim, num_corrupted_tiles))

    # Real input
    input_text = get_input_from_file("input.txt")
    dim = 71
    num_corrupted_tiles = 1024
    print(get_shortest_path_v2(input_text, dim, num_corrupted_tiles))
