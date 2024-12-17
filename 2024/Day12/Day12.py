import copy


class Region:
    area: int
    perimeter: int
    char: str

    def __init__(self, area: int, perimeter: int, char: str):
        self.area = area
        self.perimeter = perimeter
        self.char = char

    def __add__(self, other):
        return Region(self.area + other.area, self.perimeter + other.perimeter, self.char)


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def build_matrix(text: str) -> list:
    lines = text.split("\n")
    matrix = []
    for line in lines:
        matrix.append(list(line))

    return matrix


def check_dimensions(matrix: list[list[int]], dim1: int, dim2: int) -> list[int]:
    sizes = []

    for i in range(dim1-1):
        difference_row = [matrix[i+1][j] - matrix[i][j] for j in range(dim2)]
        j = 0
        while j < dim2:
            if difference_row[j] == 1:
                size = 1
                for k in range(j+1, dim2):
                    if difference_row[k] == 1:
                        size += 1
                    else:
                        break
                sizes.append(size)
                j += size
            elif difference_row[j] == -1:
                size = 1
                for k in range(j + 1, dim2):
                    if difference_row[k] == -1:
                        size += 1
                    else:
                        break
                sizes.append(size)
                j += size
            else:
                j += 1
    return sizes


def adjust_perimeter(matrix: list[list[int]]) -> list[int]:
    sizes = []
    matrix.insert(0, [0 for _ in range(len(matrix[0]))])
    matrix.append([0 for _ in range(len(matrix[0]))])
    for i in range(len(matrix)):
        matrix[i].insert(0, 0)
        matrix[i].append(0)

    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    sizes += check_dimensions(matrix, rows, cols)
    sizes += check_dimensions([[matrix[j][i] for j in range(rows)] for i in range(cols)], cols, rows)

    return sizes


def get_final_price_v2(text: str) -> int:
    res = 0

    matrix = build_matrix(text)
    computed_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if computed_matrix[i][j] == 0:
                prev_matrix = copy.deepcopy(computed_matrix)
                computed_matrix[i][j] = 1
                region, computed_matrix = get_area_and_perimeter(computed_matrix, i, j, matrix)
                difference_matrix = [[computed_matrix[i][j] - prev_matrix[i][j] for j in range(len(computed_matrix[0]))] for i in range(len(computed_matrix))]
                sizes = adjust_perimeter(difference_matrix)
                res += region.area * len(sizes)
    return res


def get_area_and_perimeter(
        computed_matrix: list[list[int]], i: int, j: int, matrix: list[list[str]]
) -> tuple[Region, list[list[int]]]:
    region = Region(1, 0, matrix[i][j])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for direction in directions:
        new_i = i + direction[0]
        new_j = j + direction[1]

        if 0 <= new_i < len(computed_matrix) and 0 <= new_j < len(computed_matrix[0]):
            if matrix[new_i][new_j] == region.char and computed_matrix[new_i][new_j] == 0:
                computed_matrix[new_i][new_j] = 1
                new_region, new_computed_matrix = get_area_and_perimeter(computed_matrix, new_i, new_j, matrix)
                region = region + new_region
                computed_matrix = new_computed_matrix
            elif matrix[new_i][new_j] != region.char:
                region.perimeter += 1
        else:
            region.perimeter += 1

    return region, computed_matrix


def get_final_price(text: str) -> int:
    res = 0

    matrix = build_matrix(text)
    computed_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if computed_matrix[i][j] == 0:
                computed_matrix[i][j] = 1
                region, computed_matrix = get_area_and_perimeter(computed_matrix, i, j, matrix)
                res += region.area * region.perimeter
    return res


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_final_price(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_final_price(input_text))

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_final_price_v2(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_final_price_v2(input_text))
