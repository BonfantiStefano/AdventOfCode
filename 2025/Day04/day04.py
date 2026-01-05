from copy import deepcopy

LEN_BATTERY = 12


def get_input_from_file(filename: str) -> list[list[str]]:
    """
    This function reads the input from a file and return the list of ids pairs.

    Returns
    ------
    A list of ìds pairs
    """

    # Open the file
    with open(filename, "r") as file:
        # Read the lines
        lines = file.readlines()

    return [[char for char in line.strip()] for line in lines]


def _check_element(matrix: list[list[str]], x: int, y: int) -> bool:
    current_value = matrix[y][x]
    if current_value != '@':
        return False

    available_directions = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1)
    ]

    counter = 0
    for dx, dy in available_directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
            if matrix[ny][nx] == '@':
                counter += 1
        if counter >= 4:
            return False
    return True


if __name__ == "__main__":
    input_matrix = get_input_from_file("./input.txt")
    resulting_matrix = deepcopy(input_matrix)

    WIDTH = len(input_matrix[0])
    HEIGHT = len(input_matrix)

    res = 0
    count_at = sum(line.count('@') for line in input_matrix)
    print(f'Initial count of @: {count_at}')
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if _check_element(input_matrix, i, j):
                res += 1
                resulting_matrix[j][i] = 'x'

    updated_count_at = sum(line.count('@') for line in resulting_matrix)
    print(f'Updated count of @: {updated_count_at}')
    while updated_count_at != count_at:
        count_at = updated_count_at
        input_matrix = deepcopy(resulting_matrix)
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if _check_element(input_matrix, i, j):
                    res += 1
                    resulting_matrix[j][i] = 'x'
        updated_count_at = sum(line.count('@') for line in resulting_matrix)
        print(f'Updated count of @: {updated_count_at}')

    print(res)
    for line in resulting_matrix:
        print(''.join(line))
