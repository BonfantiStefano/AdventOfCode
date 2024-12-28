import sys

def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def build_maze(text: str) -> list[list[str]]:
    lines = text.split("\n")
    maze = []
    for line in lines:
        maze.append(list(line))

    return maze


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


def get_cheat_neighbors(pos: tuple[int, int], distance_matrix: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)

    directions = [up, down, left, right]
    valid_directions = []
    for dir in directions:
        if (pos[0]+dir[0], pos[1]+dir[1]) not in distance_matrix and (pos[0]+2*dir[0], pos[1]+2*dir[1]) in distance_matrix and distance_matrix[(pos[0]+2*dir[0], pos[1]+2*dir[1])] > distance_matrix[pos] + 2:
            valid_directions.append((pos[0]+2*dir[0], pos[1]+2*dir[1]))

    return valid_directions


def dijkstra(
        maze: list[list[str]], start: tuple[int, int]
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

    distance_matrix[start] = 0

    previous_matrix[start] = start

    to_analyze = [start]
    while len(to_analyze) > 0:
        pos = to_analyze.pop(0)
        neighbors = get_neighbors(pos, maze)
        neighbors.sort(key=lambda n: distance_matrix[n])
        for neighbor in neighbors:
            if visited_matrix[neighbor]:
                continue
            if neighbor not in to_analyze and maze[neighbor[0]][neighbor[1]] != 'E':
                to_analyze.append(neighbor)
            actual_distance = distance_matrix[pos] + 1
            if actual_distance < distance_matrix[neighbor]:
                # maze[neighbor[0]][neighbor[1]] = 'x'
                # for x in range(len(maze[0])):
                #     for y in range(len(maze)):
                #         print(maze[x][y], end="")
                #     print()
                distance_matrix[neighbor] = actual_distance
                previous_matrix[neighbor] = pos
        visited_matrix[pos] = True
        to_analyze.sort(key=lambda n: distance_matrix[n])

    return distance_matrix


def valuable_cheats(cheats: dict[int, int], threshold: int) -> int:
    res = 0
    for key, value in cheats.items():
        if key >= threshold:
            res += value

    return res


def get_cheat_neighbors_v2(
        pos: tuple[int, int], distance_matrix: dict[tuple[int, int], int], width: int, height: int
) -> list[tuple[int, int, int]]:
    x0, y0 = pos
    max_distance = 20
    valid_cheats = []

    for dx in range(-max_distance, max_distance + 1):
        for dy in range(-max_distance + abs(dx), max_distance - abs(dx) + 1):
            nx, ny = x0 + dx, y0 + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) in distance_matrix and distance_matrix[(nx, ny)] > distance_matrix[pos] + abs(dx) + abs(dy):
                valid_cheats.append((nx, ny, distance_matrix[(nx, ny)] - distance_matrix[pos] - abs(dx) - abs(dy)))

    return valid_cheats


def get_massive_cheats_v2(text: str, threshold: int) -> int:
    maze = build_maze(text)

    for x in range(len(maze[0])):
        for y in range(len(maze)):
            if maze[x][y] == 'S':
                start = (x, y)
                break

    cheats = {}
    visited = {}
    distance_matrix = dijkstra(maze, start)

    # Sort distance_matrix by distance
    distance_matrix = dict(sorted(distance_matrix.items(), key=lambda item: item[1]))

    for point, distance in distance_matrix.items():
        cheats_neighbors = get_cheat_neighbors_v2(point, distance_matrix, len(maze[0]), len(maze))
        for x_neighbor, y_neighbor, n_distance in cheats_neighbors:
            # if (x_neighbor, y_neighbor) not in visited:
            #     visited[(x_neighbor, y_neighbor)] = 1
            if n_distance not in cheats:
                cheats[n_distance] = 1
            else:
                cheats[n_distance] += 1

    print(cheats)
    res = valuable_cheats(cheats, threshold)
    return res


def get_massive_cheats(text: str, threshold: int) -> int:
    maze = build_maze(text)

    for x in range(len(maze[0])):
        for y in range(len(maze)):
            print(maze[x][y], end="")
        print()

    for x in range(len(maze[0])):
        for y in range(len(maze)):
            if maze[x][y] == 'S':
                start = (x, y)
                break

    cheats = {}
    distance_matrix = dijkstra(maze, start)
    # for point, distance in distance_matrix.items():
    #     print(point, distance)

    for point, distance in distance_matrix.items():
        cheats_neighbors = get_cheat_neighbors(point, distance_matrix)
        for neighbor in cheats_neighbors:
            new_distance = distance_matrix[neighbor]
            if new_distance - distance - 2 not in cheats:
                cheats[new_distance-distance - 2] = 1
            else:
                cheats[new_distance-distance - 2] += 1

    print(cheats)
    res = valuable_cheats(cheats, threshold)
    return res


if __name__ == "__main__":
    # # Example
    # input_text = get_input_from_file("example.txt")
    # min_t = 10
    # print(get_massive_cheats(input_text, min_t))

    # # Real input
    # input_text = get_input_from_file("input.txt")
    # min_t = 100
    # print(get_massive_cheats(input_text, min_t))

    # # Part 2
    # # Example
    # input_text = get_input_from_file("example.txt")
    # min_t = 50
    # print(get_massive_cheats_v2(input_text, min_t))

    # Real input
    input_text = get_input_from_file("input.txt")
    min_t = 100
    print(get_massive_cheats_v2(input_text, min_t))
