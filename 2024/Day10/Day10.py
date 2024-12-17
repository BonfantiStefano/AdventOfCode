def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def get_topographic_map(text: str) -> list[list[int]]:
    map_list = text.split("\n")
    top_map = []
    for ml in map_list:
        line = []
        for elem in ml:
            line.append(int(elem))
        top_map.append(line)
    return top_map


def count_trailheads(matrix: list[list[int]], i: int, j: int, heads_reached: list[tuple[int, int]]) -> int:
    res = 0

    if matrix[i][j] == 9 and (i, j) not in heads_reached:
        heads_reached.append((i, j))
        return 1

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for d in directions:
        new_i = i + d[0]
        new_j = j + d[1]

        if 0 <= new_i < len(matrix) and 0 <= new_j < len(matrix[0]) and matrix[new_i][new_j] == matrix[i][j] + 1:
            res += count_trailheads(matrix, new_i, new_j, heads_reached)

    return res


def get_num_trailheads(text: str) -> int:
    trailheads = 0

    matrix = get_topographic_map(text)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                heads_reached = []
                trailheads += count_trailheads(matrix, i, j, heads_reached)

    return trailheads


def count_trailheads_v2(matrix: list[list[int]], i: int, j: int) -> int:
    res = 0

    if matrix[i][j] == 9:
        return 1

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for d in directions:
        new_i = i + d[0]
        new_j = j + d[1]

        if 0 <= new_i < len(matrix) and 0 <= new_j < len(matrix[0]) and matrix[new_i][new_j] == matrix[i][j] + 1:
            res += count_trailheads_v2(matrix, new_i, new_j)

    return res


def get_num_trailheads_v2(text: str) -> int:
    trailheads = 0

    matrix = get_topographic_map(text)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                heads_reached = []
                trailheads += count_trailheads_v2(matrix, i, j)

    return trailheads


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_num_trailheads(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_num_trailheads(input_text))

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_num_trailheads_v2(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_num_trailheads_v2(input_text))
