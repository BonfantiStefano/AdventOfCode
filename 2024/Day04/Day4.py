def get_dir_from_idx(idx: int) -> tuple[int, int]:
    match idx:
        case 0:
            return -1, -1
        case 1:
            return -1, 0
        case 2:
            return -1, 1
        case 3:
            return 0, -1
        case 4:
            return 0, 1
        case 5:
            return 1, -1
        case 6:
            return 1, 0
        case 7:
            return 1, 1
        case _:
            raise ValueError("Invalid index")


def get_char_from_idx(idx: int) -> str:
    match idx:
        case 0:
            return "M"
        case 1:
            return "A"
        case 2:
            return "S"
        case _:
            raise ValueError("Invalid index")


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def check_value(i, j, matrix: list[list[str]], char: int, direction: int) -> bool:
    x = i + get_dir_from_idx(direction)[0]
    y = j + get_dir_from_idx(direction)[1]
    if (0 <= x < len(matrix) and 0 <= y < len(matrix[0])
            and matrix[x][y] == get_char_from_idx(char)):
        if char == 2:
            return True
        return check_value(x, y, matrix, char=char + 1, direction=direction)
    else:
        return False


def check_surroundings(i, j, matrix: list[list[str]]) -> bool:
    if (check_value(i - 2*get_dir_from_idx(7)[0], j - 2*get_dir_from_idx(7)[1], matrix, char=0, direction=7) or
            check_value(i - 2*get_dir_from_idx(0)[0], j - 2*get_dir_from_idx(0)[1], matrix, char=0, direction=0)):
        if (check_value(i - 2*get_dir_from_idx(2)[0], j - 2*get_dir_from_idx(2)[1], matrix, char=0, direction=2) or
                check_value(i - 2*get_dir_from_idx(5)[0], j - 2*get_dir_from_idx(5)[1], matrix, char=0, direction=5)):
            return True
    return False


def find_xmas(matrix: list[str]) -> int:
    list_of_lists = [list(string) for string in matrix]
    res = 0

    for x, line in enumerate(list_of_lists):
        for y, char in enumerate(line):
            if char == "X":
                values = []
                for idx in range(8):
                    values.append(check_value(x, y, list_of_lists, direction=idx, char=0))
                res += values.count(True)
    return res


def find_x_mas(matrix: list[str]) -> int:
    list_of_lists = [list(string) for string in matrix]
    res = 0

    for x, line in enumerate(list_of_lists):
        for y, char in enumerate(line):
            if char == "A":
                if check_surroundings(x, y, list_of_lists):
                    res += 1
    return res


if __name__ == "__main__":
    # Example
    matrix_xmas = [
        'MMMSXXMASM',
        'MSAMXMSMSA',
        'AMXSXMAAMM',
        'MSAMASMSMX',
        'XMASAMXAMM',
        'XXAMMXXAMA',
        'SMSMSASXSS',
        'SAXAMASAAA',
        'MAMMMXMMMM',
        'MXMXAXMASX',
    ]
    print(find_xmas(matrix_xmas))

    # Real input
    matrix_xmas = get_input_from_file("input.txt")
    matrix_xmas = matrix_xmas.split("\n")
    print(find_xmas(matrix_xmas))

    # Part 2
    # Example
    matrix_xmas = [
        'MMMSXXMASM',
        'MSAMXMSMSA',
        'AMXSXMAAMM',
        'MSAMASMSMX',
        'XMASAMXAMM',
        'XXAMMXXAMA',
        'SMSMSASXSS',
        'SAXAMASAAA',
        'MAMMMXMMMM',
        'MXMXAXMASX',
    ]
    print(find_x_mas(matrix_xmas))

    # Real input
    matrix_xmas = get_input_from_file("input.txt")
    matrix_xmas = matrix_xmas.split("\n")
    print(find_x_mas(matrix_xmas))
