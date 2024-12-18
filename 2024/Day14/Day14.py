EXAMPLE_X = 7
EXAMPLE_Y = 11
INPUT_X = 103
INPUT_Y = 101


class Robot:
    pos_x: int
    pos_y: int
    vel_x: int
    vel_y: int

    def __init__(self, pos_x: int, pos_y: int, vel_x: int, vel_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def __str__(self):
        return f"Robot: Pos=({self.pos_x}, {self.pos_y}), Vel=({self.vel_x}, {self.vel_y})"


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def build_robots(text: str) -> list[Robot]:
    robot_lists = text.split("\n")
    robots = []
    for robot in robot_lists:
        pos, vel = robot.split(" ")
        pos_x, pos_y = (int(pos.split(",")[1]), int(pos.split(",")[0].strip("p=")))
        vel_x, vel_y = (int(vel.split(",")[1]), int(vel.split(",")[0].strip("v=")))
        robots.append(Robot(pos_x=pos_x, pos_y=pos_y, vel_x=vel_x, vel_y=vel_y))

    return robots


def check_quadrants(matrix: list[list[str]]) -> int:
    res = 1
    size_quadrant_x = len(matrix) // 2
    size_quadrant_y = len(matrix[0]) // 2
    starting_points_quadrants = [(0, 0), (0, len(matrix[0]) // 2 + 1), (len(matrix) // 2 + 1, 0),
                                 (len(matrix) // 2 + 1, len(matrix[0]) // 2 + 1)]

    for starting_point in starting_points_quadrants:
        partial_res = 0
        for i in range(size_quadrant_x):
            for j in range(size_quadrant_y):
                if matrix[starting_point[0] + i][starting_point[1] + j] != ".":
                    partial_res += int(matrix[starting_point[0] + i][starting_point[1] + j])

        if partial_res > 0:
            res *= partial_res

    return res


def predict_robots(text: str, rows: int, cols: int) -> int:
    robots = build_robots(text)

    # for robot in robots:
    #     print(robot)

    for step in range(1, 101):
        for robot in robots:
            robot.pos_x = (robot.pos_x + robot.vel_x) % rows
            robot.pos_y = (robot.pos_y + robot.vel_y) % cols

    matrix = [["." for _ in range(cols)] for _ in range(rows)]
    for robot in robots:
        if matrix[robot.pos_x][robot.pos_y] == ".":
            matrix[robot.pos_x][robot.pos_y] = "1"
        else:
            matrix[robot.pos_x][robot.pos_y] = str(int(matrix[robot.pos_x][robot.pos_y]) + 1)

    # for row in matrix:
    #     print(row)

    res = check_quadrants(matrix)

    return res


def analyze_matrix(matrix: list[list[str]]) -> bool:
    # look for a dense area of robots
    neighbors = 0
    neighborhood = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != ".":
                for neighbor in neighborhood:
                    if 0 <= i + neighbor[0] < len(matrix) and 0 <= j + neighbor[1] < len(matrix[0]):
                        if matrix[i + neighbor[0]][j + neighbor[1]] != ".":
                            neighbors += 1

    if neighbors >= 500:
        return True


def predict_robots_v2(text: str, rows: int, cols: int) -> int:
    robots = build_robots(text)

    # for robot in robots:
    #     print(robot)

    matrix = [["." for _ in range(cols)] for _ in range(rows)]
    for robot in robots:
        if matrix[robot.pos_x][robot.pos_y] == ".":
            matrix[robot.pos_x][robot.pos_y] = "1"
        else:
            matrix[robot.pos_x][robot.pos_y] = str(int(matrix[robot.pos_x][robot.pos_y]) + 1)

    for step in range(1, 10000):
        for robot in robots:
            if matrix[robot.pos_x][robot.pos_y] == "1":
                matrix[robot.pos_x][robot.pos_y] = "."
            else:
                matrix[robot.pos_x][robot.pos_y] = str(int(matrix[robot.pos_x][robot.pos_y]) - 1)
            robot.pos_x = (robot.pos_x + robot.vel_x) % rows
            robot.pos_y = (robot.pos_y + robot.vel_y) % cols
            if matrix[robot.pos_x][robot.pos_y] == ".":
                matrix[robot.pos_x][robot.pos_y] = "1"
            else:
                matrix[robot.pos_x][robot.pos_y] = str(int(matrix[robot.pos_x][robot.pos_y]) + 1)

        if analyze_matrix(matrix):
            print(f"Step: {step}")
            for row in matrix:
                for elem in row:
                    print(elem, end="")
                print("\n")
            print("\n\n###################################################################\n\n")

    return 0


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    dim1 = EXAMPLE_X
    dim2 = EXAMPLE_Y
    print(predict_robots(input_text, dim1, dim2))

    # Real input
    input_text = get_input_from_file("input.txt")
    dim1 = INPUT_X
    dim2 = INPUT_Y
    print(predict_robots(input_text, dim1, dim2))

    # Part2
    # Real input
    input_text = get_input_from_file("input.txt")
    dim1 = INPUT_X
    dim2 = INPUT_Y
    print(predict_robots_v2(input_text, dim1, dim2))
