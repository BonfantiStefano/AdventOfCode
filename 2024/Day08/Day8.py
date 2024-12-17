class Antenna:
    def __init__(self, x: int, y: int, antenna_type: str):
        self.x = x
        self.y = y
        self.antenna_type = antenna_type


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def build_matrix(text: str) -> list:
    lines = text.split("\n")
    matrix = []
    for line in lines:
        matrix.append(list(line))

    return matrix


def get_antennas(matrix: list[list[str]]) -> list[Antenna]:
    antennas = []
    for i, line in enumerate(matrix):
        for j, char in enumerate(line):
            if char != '.':
                antennas.append(Antenna(i, j, char))

    return antennas


def compute_antinodes(antenna1: Antenna, antenna2: Antenna, matrix: list[list[str]]) -> tuple[int, list[list[str]]]:
    x_distance = antenna2.x - antenna1.x
    y_distance = antenna2.y - antenna1.y
    antinodes = 0
    ideal_new_pos1 = (antenna1.x - x_distance, antenna1.y - y_distance)
    ideal_new_pos2 = (antenna2.x + x_distance, antenna2.y + y_distance)
    if 0 <= ideal_new_pos1[0] < len(matrix) and 0 <= ideal_new_pos1[1] < len(matrix[0]):
        if matrix[ideal_new_pos1[0]][ideal_new_pos1[1]] != "#":
            antinodes += 1
            matrix[ideal_new_pos1[0]][ideal_new_pos1[1]] = "#"
    if 0 <= ideal_new_pos2[0] < len(matrix) and 0 <= ideal_new_pos2[1] < len(matrix[0]):
        if matrix[ideal_new_pos2[0]][ideal_new_pos2[1]] != "#":
            antinodes += 1
            matrix[ideal_new_pos2[0]][ideal_new_pos2[1]] = "#"

    return antinodes, matrix


def calculate_antinodes(text: str) -> int:
    # Parse the input
    matrix = build_matrix(text)

    # Get the number and type of antennas
    antennas = get_antennas(matrix)

    # Calculate the number of antinodes
    antinodes = 0

    for idx, antenna in enumerate(antennas[:-1]):
        for other_antenna in antennas[idx+1:]:
            if antenna.antenna_type == other_antenna.antenna_type:
                new_antinodes, matrix = compute_antinodes(antenna, other_antenna, matrix)
                antinodes += new_antinodes

    # with open("output.txt", "w") as file:
    #     for row in matrix:
    #         file.write("".join(row) + "\n")
    return antinodes


def compute_antinodes_v2(antenna1: Antenna, antenna2: Antenna, matrix: list[list[str]]) -> tuple[int, list[list[str]]]:
    x_distance = antenna2.x - antenna1.x
    y_distance = antenna2.y - antenna1.y
    antinodes = 0

    ideal_new_pos1 = (antenna1.x - x_distance, antenna1.y - y_distance)
    while 0 <= ideal_new_pos1[0] < len(matrix) and 0 <= ideal_new_pos1[1] < len(matrix[0]):
        if matrix[ideal_new_pos1[0]][ideal_new_pos1[1]] != "#":
            antinodes += 1
            matrix[ideal_new_pos1[0]][ideal_new_pos1[1]] = "#"
        ideal_new_pos1 = (ideal_new_pos1[0] - x_distance, ideal_new_pos1[1] - y_distance)

    ideal_new_pos2 = (antenna2.x + x_distance, antenna2.y + y_distance)
    while 0 <= ideal_new_pos2[0] < len(matrix) and 0 <= ideal_new_pos2[1] < len(matrix[0]):
        if matrix[ideal_new_pos2[0]][ideal_new_pos2[1]] != "#":
            antinodes += 1
            matrix[ideal_new_pos2[0]][ideal_new_pos2[1]] = "#"
        ideal_new_pos2 = (ideal_new_pos2[0] + x_distance, ideal_new_pos2[1] + y_distance)

    if matrix[antenna1.x][antenna1.y] != "#":
        matrix[antenna1.x][antenna1.y] = "#"
        antinodes += 1

    if matrix[antenna2.x][antenna2.y] != "#":
        matrix[antenna2.x][antenna2.y] = "#"
        antinodes += 1

    return antinodes, matrix


def calculate_antinodes_v2(text: str) -> int:
    # Parse the input
    matrix = build_matrix(text)

    # Get the number and type of antennas
    antennas = get_antennas(matrix)

    # Calculate the number of antinodes
    antinodes = 0

    for idx, antenna in enumerate(antennas[:-1]):
        for other_antenna in antennas[idx+1:]:
            if antenna.antenna_type == other_antenna.antenna_type:
                new_antinodes, matrix = compute_antinodes_v2(antenna, other_antenna, matrix)
                antinodes += new_antinodes

    # with open("output.txt", "w") as file:
    #     for row in matrix:
    #         file.write("".join(row) + "\n")
    return antinodes


if __name__ == "__main__":
    # # Example
    # input_text = get_input_from_file("example.txt")
    # print(calculate_antinodes(input_text))
    #
    # # Real input
    # input_text = get_input_from_file("input.txt")
    # print(calculate_antinodes(input_text))

    # # Part 2
    # # Example
    # input_text = get_input_from_file("example.txt")
    # print(calculate_antinodes_v2(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(calculate_antinodes_v2(input_text))
