from collections import deque
import sys


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def build_matrix(text: str) -> list[list[str]]:
    maze = text.split("\n")

    matrix = []
    for line in maze:
        matrix.append(list(line))

    return matrix


class Direction:
    EAST = (1, 0)
    NORTH = (0, -1)
    WEST = (-1, 0)
    SOUTH = (0, 1)


def turn(direction: tuple[int, int], towards: str):
    if towards != 'left' and towards != 'right':
        raise RuntimeError('ERROR: Invalid turning direction')
    match direction:
        case Direction.EAST:
            return Direction.NORTH if towards == 'left' else Direction.SOUTH
        case Direction.NORTH:
            return Direction.WEST if towards == 'left' else Direction.EAST
        case Direction.WEST:
            return Direction.SOUTH if towards == 'left' else Direction.NORTH
        case Direction.SOUTH:
            return Direction.EAST if towards == 'left' else Direction.WEST
        case _:
            raise RuntimeError('ERROR: Invalid direction')


def get_neighbors(pos: tuple[int, int, tuple[int, int]]) -> list[tuple[int, int, tuple[int, int]]]:
    forward = (pos[0] + pos[2][0], pos[1] + pos[2][1], pos[2])
    left = (pos[0], pos[1], turn(pos[2], 'left'))
    right = (pos[0], pos[1], turn(pos[2], 'right'))

    return [forward, left, right]


def dijkstra(
        maze: list[list[str]]
) -> tuple[dict[tuple[int, int, tuple[int, int]], int],
dict[tuple[int, int, tuple[int, int]], None | list[tuple[int, int, tuple[int, int]]]]]:
    width = len(maze[0])
    height = len(maze)

    distance_matrix = {
        (x, y, d): sys.maxsize
        for x in range(width)
        for y in range(height)
        for d in [Direction.EAST, Direction.NORTH, Direction.WEST, Direction.SOUTH]
    }
    distance_matrix[(1, height - 2, Direction.EAST)] = 0

    visited_matrix = {
        (x, y, d): False
        for x in range(width)
        for y in range(height)
        for d in [Direction.EAST, Direction.NORTH, Direction.WEST, Direction.SOUTH]
    }

    paths_matrix: dict[tuple[int, int, tuple[int, int]], None | list[tuple[int, int, tuple[int, int]]]] = {
        (x, y, d): None
        for x in range(width)
        for y in range(height)
        for d in [Direction.EAST, Direction.NORTH, Direction.WEST, Direction.SOUTH]
    }
    paths_matrix[(1, height - 2, Direction.EAST)] = []

    to_analyze = [(1, height - 2, Direction.EAST)]
    while len(to_analyze) > 0:
        pos = to_analyze.pop(0)
        neighbors = get_neighbors(pos)
        neighbors.sort(key=lambda n: distance_matrix[n])
        for neighbor in neighbors:
            if visited_matrix[neighbor] or maze[neighbor[1]][neighbor[0]] == '#':
                continue
            if neighbor not in to_analyze and maze[neighbor[1]][neighbor[0]] != 'E':
                to_analyze.append(neighbor)
            actual_distance = distance_matrix[pos]
            if pos[0] == neighbor[0] and pos[1] == neighbor[1]:
                actual_distance += 1000
            else:
                actual_distance += 1
            if actual_distance < distance_matrix[neighbor]:
                distance_matrix[neighbor] = actual_distance
                paths_matrix[neighbor] = [pos]
            elif actual_distance == distance_matrix[neighbor]:
                paths_matrix[neighbor].append(pos)
        visited_matrix[pos] = True
        to_analyze.sort(key=lambda n: distance_matrix[n])

    return distance_matrix, paths_matrix


def get_shortest_path(text: str) -> int:
    maze = build_matrix(text)

    dist, pred = dijkstra(maze)

    score1 = dist[(len(maze[0]) - 2, 1, Direction.EAST)]
    score2 = dist[(len(maze[0]) - 2, 1, Direction.NORTH)]

    min_score = score1 if score1 < score2 else score2
    return min_score


def get_covered_tiles(text: str) -> int:
    maze = build_matrix(text)

    dist, pred = dijkstra(maze)

    end_1 = (len(maze[0]) - 2, 1, Direction.EAST)
    end_2 = (len(maze[0]) - 2, 1, Direction.NORTH)

    end_dist_1 = dist[end_1]
    end_dist_2 = dist[end_2]

    q = deque()
    if end_dist_1 <= end_dist_2:
        q.append(end_1)
    if end_dist_1 >= end_dist_2:
        q.append(end_2)

    tiles = set()
    while len(q) != 0:
        p = q.popleft()
        tiles.add(p[:2])
        for v in pred[p]:
            q.append(v)

    return len(tiles)


if __name__ == "__main__":
    # # Example
    # input_text = get_input_from_file("example.txt")
    # print(get_shortest_path(input_text))
    #
    # # Example 2
    # input_text = get_input_from_file("example2.txt")
    # print(get_shortest_path(input_text))
    #
    # # Real input
    # input_text = get_input_from_file("input.txt")
    # print(get_shortest_path(input_text))

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_covered_tiles(input_text))

    # Example 2
    input_text = get_input_from_file("example2.txt")
    print(get_covered_tiles(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_covered_tiles(input_text))
