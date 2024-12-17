import copy


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def build_matrix(text: str) -> list:
    lines = text.split("\n")
    matrix = []
    for line in lines:
        matrix.append(list(line))

    return matrix


def get_move_from_direction(direction: int) -> tuple:
    if direction == 0:
        return -1, 0
    elif direction == 1:
        return 0, 1
    elif direction == 2:
        return 1, 0
    elif direction == 3:
        return 0, -1


def count_steps(text: str) -> tuple[int, list[list[str]]]:
    res = 0

    matrix = build_matrix(text)
    steps_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    movement_matrix = matrix.copy()

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "^":
                starting_pos = (i, j)

    steps_matrix[starting_pos[0]][starting_pos[1]] = 1

    is_done = False
    direction = 0
    current_pos = starting_pos
    has_turned = False
    while is_done is False:
        ideal_new_pos = (current_pos[0] + get_move_from_direction(direction)[0], current_pos[1] + get_move_from_direction(direction)[1])
        if ideal_new_pos[0] < 0 or ideal_new_pos[0] >= len(matrix) or ideal_new_pos[1] < 0 or ideal_new_pos[1] >= len(matrix[0]):
            movement_matrix[current_pos[0]][current_pos[1]] = "|" if direction % 2 == 0 else "-"
            is_done = True
        elif matrix[ideal_new_pos[0]][ideal_new_pos[1]] == "#":
            has_turned = True
            movement_matrix[current_pos[0]][current_pos[1]] = "+"
            direction = (direction + 1) % 4
        else:
            steps_matrix[ideal_new_pos[0]][ideal_new_pos[1]] = 1
            if current_pos != starting_pos and has_turned is False:
                movement_matrix[current_pos[0]][current_pos[1]] = "|" if direction % 2 == 0 else "-"
            if has_turned:
                has_turned = False
            current_pos = ideal_new_pos

    for i in range(len(steps_matrix)):
        for j in range(len(steps_matrix[i])):
            if steps_matrix[i][j] == 1:
                res += 1

    with open("output.txt", "w") as file:
        for row in movement_matrix:
            file.write("".join(row) + "\n")
    return res, movement_matrix


def get_new_obstacle_pos(movement_matrix: list[list[str]]) -> tuple[int, int]:
    for i in range(len(movement_matrix)):
        for j in range(len(movement_matrix[i])):
            if movement_matrix[i][j] in ["|", "-", "+"]:
                return i, j


def check_loop(matrix: list[list[str]], starting_pos: tuple[int, int]) -> bool:
    is_done = False
    direction = 0
    current_pos = starting_pos
    turning_pos = []
    turning_dir = []
    is_loop = False
    has_turned = False
    while is_done is False and is_loop is False:
        ideal_new_pos = (current_pos[0] + get_move_from_direction(direction)[0], current_pos[1] + get_move_from_direction(direction)[1])
        if ideal_new_pos[0] < 0 or ideal_new_pos[0] >= len(matrix) or ideal_new_pos[1] < 0 or ideal_new_pos[1] >= len(matrix[0]):
            is_done = True
        elif matrix[ideal_new_pos[0]][ideal_new_pos[1]] == "#":
            has_turned = True
            matrix[current_pos[0]][current_pos[1]] = "+"
            if current_pos in turning_pos:
                idx = turning_pos.index(current_pos)
                if turning_dir[idx] == direction:
                    is_loop = True
            else:
                turning_pos.append(current_pos)
                turning_dir.append(direction)
            direction = (direction + 1) % 4
        else:
            if current_pos != starting_pos and has_turned is False:
                if matrix[current_pos[0]][current_pos[1]] in ["|", "-"]:
                    matrix[current_pos[0]][current_pos[1]] = "+"
                else:
                    matrix[current_pos[0]][current_pos[1]] = "|" if direction % 2 == 0 else "-"
            if has_turned:
                has_turned = False
            current_pos = ideal_new_pos

    return is_loop


def count_loops(text: str) -> int:
    res = 0

    num_trials, movement_matrix = count_steps(text)
    # remove the starting position
    num_trials -= 1
    matrix = build_matrix(text)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "^":
                starting_pos = (i, j)

    movement_matrix[starting_pos[0]][starting_pos[1]] = "X"

    for i in range(num_trials):
        print("Start trial: ", i)
        new_obstacle_pos = get_new_obstacle_pos(movement_matrix)
        new_matrix = copy.deepcopy(matrix)
        new_matrix[new_obstacle_pos[0]][new_obstacle_pos[1]] = "#"

        if check_loop(new_matrix, starting_pos):
            res += 1
            print(f"Loop found: {new_obstacle_pos}")
        movement_matrix[new_obstacle_pos[0]][new_obstacle_pos[1]] = "X"
        print("End trial: ", i)
    return res


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    print(count_steps(input_text)[0])

    # Real input
    input_text = get_input_from_file("input.txt")
    print(count_steps(input_text)[0])

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    print(count_loops(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(count_loops(input_text))
