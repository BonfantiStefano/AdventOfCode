import copy

def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def get_direction_from_move(move: str) -> tuple[int, int]:
    if move == "^":
        return -1, 0
    elif move == "v":
        return 1, 0
    elif move == "<":
        return 0, -1
    elif move == ">":
        return 0, 1
    else:
        raise ValueError(f"Invalid move: {move}")


def build_matrix_and_moves(text: str) -> tuple[list[list[str]], list[str]]:
    warehouse_map, moves = text.split("\n\n")

    lines = warehouse_map.split("\n")
    matrix = []
    for line in lines:
        matrix.append(list(line))

    lines = moves.split("\n")
    moves = []
    for line in lines:
        for elem in line:
            moves.append(elem)

    return matrix, moves


def check_matrix(matrix: list[list[str]]) -> int:
    res = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "O":
                res += 100 * i + j
    return res


def update_matrix(matrix: list[list[str]], pos: tuple[int, int], move: str) -> tuple[list[list[str]], tuple[int, int]]:
    x, y = pos
    dx, dy = get_direction_from_move(move)
    new_x, new_y = x + dx, y + dy

    if matrix[new_x][new_y] == "#":
        return matrix, pos
    if matrix[new_x][new_y] == ".":
        matrix[new_x][new_y] = "@"
        matrix[x][y] = "."
        return matrix, (new_x, new_y)

    ideal_x, ideal_y = new_x, new_y
    step = 0
    while matrix[ideal_x][ideal_y] == "O":
        ideal_x += dx
        ideal_y += dy
        step += 1

    if matrix[ideal_x][ideal_y] == "#":
        return matrix, pos
    if matrix[ideal_x][ideal_y] == ".":
        ideal_x, ideal_y = new_x, new_y
        for i in range(step):
            ideal_x += dx
            ideal_y += dy
            matrix[ideal_x][ideal_y] = "O"
        matrix[new_x][new_y] = "@"
        matrix[x][y] = "."
        return matrix, (new_x, new_y)


def get_gps_sum(text: str) -> int:
    matrix, moves = build_matrix_and_moves(text)

    # for line in matrix:
    #     print(line)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "@":
                pos = (i, j)
                break

    for move in moves:
        matrix, pos = update_matrix(matrix, pos, move)

    res = check_matrix(matrix)

    return res


def enlarge_matrix(matrix: list[list[str]]) -> list[list[str]]:
    new_matrix = []
    for line in matrix:
        new_line = []
        for elem in line:
            if elem == "#":
                new_line.append("#")
                new_line.append("#")
            elif elem == "@":
                new_line.append("@")
                new_line.append(".")
            elif elem == 'O':
                new_line.append("[")
                new_line.append("]")
            else:
                new_line.append(".")
                new_line.append(".")
        new_matrix.append(new_line)
    return new_matrix


def update_matrix_v2(matrix: list[list[str]], pos: tuple[int, int], move: str) -> tuple[list[list[str]], tuple[int, int]]:
    x, y = pos
    dx, dy = get_direction_from_move(move)
    new_x, new_y = x + dx, y + dy

    if matrix[new_x][new_y] == "#":
        return matrix, pos
    if matrix[new_x][new_y] == ".":
        matrix[new_x][new_y] = "@"
        matrix[x][y] = "."
        return matrix, (new_x, new_y)

    if matrix[new_x][new_y] == "[" or matrix[new_x][new_y] == "]":
        res, visited = check_possibility_to_move(matrix, x, y, dx, dy)
        if res:
            matrix = move_block(matrix, visited, dx, dy)
            return matrix, (new_x, new_y)
    return matrix, pos


def check_possibility_to_move(
        matrix: list[list[str]], x: int, y: int, dx: int, dy: int, visited: list[list[int]] = None
) -> tuple[bool, list[list[int]]]:
    if visited is None:
        visited = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    ideal_x, ideal_y = x + dx, y + dy

    if matrix[ideal_x][ideal_y] == "#":
        return False, visited
    if matrix[ideal_x][ideal_y] == "[":
        visited[x][y] = 1
        res1, visited = check_possibility_to_move(matrix, ideal_x, ideal_y, dx, dy, visited)
        if res1 and dy != 1 and visited[ideal_x][ideal_y+1] == 0:
            return check_possibility_to_move(matrix, ideal_x, ideal_y+1, dx, dy, visited)
        if res1:
            return True, visited
        return False, visited
    if matrix[ideal_x][ideal_y] == "]":
        visited[x][y] = 1
        res1, visited = check_possibility_to_move(matrix, ideal_x, ideal_y, dx, dy, visited)
        if res1 and dy != -1 and visited[ideal_x][ideal_y-1] == 0:
            return check_possibility_to_move(matrix, ideal_x, ideal_y-1, dx, dy, visited)
        if res1:
            return True, visited
        return False, visited
    if matrix[ideal_x][ideal_y] == ".":
        visited[x][y] = 1
        if matrix[x][y] == "[" and visited[x][y+1] == 0:
            return check_possibility_to_move(matrix, x, y+1, dx, dy, visited)
        if matrix[x][y] == "]" and visited[x][y-1] == 0:
            return check_possibility_to_move(matrix, x, y-1, dx, dy, visited)
        return True, visited


def move_block(matrix: list[list[str]], visited: list[list[int]], dx: int, dy: int) -> list[list[str]]:
    matrix_copy = copy.deepcopy(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if visited[i][j] == 1:
                matrix[i+dx][j+dy] = matrix_copy[i][j]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if visited[i][j] == 1 and visited[i-dx][j-dy] == 0:
                matrix[i][j] = "."

    return matrix


def check_matrix_v2(matrix: list[list[str]]) -> int:
    res = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "[":
                res += 100 * i + j
    return res


def get_gps_sum_v2(text: str) -> int:
    matrix, moves = build_matrix_and_moves(text)

    matrix = enlarge_matrix(matrix)

    # for line in matrix:
    #     for elem in line:
    #         print(elem, end="")
    #     print()

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "@":
                pos = (i, j)
                break

    for move in moves:
        matrix, pos = update_matrix_v2(matrix, pos, move)

    res = check_matrix_v2(matrix)

    return res


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_gps_sum(input_text))

    # Example 2
    input_text = get_input_from_file("example2.txt")
    print(get_gps_sum(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_gps_sum(input_text))

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_gps_sum_v2(input_text))

    # Example 2
    input_text = get_input_from_file("example2.txt")
    print(get_gps_sum_v2(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_gps_sum_v2(input_text))
