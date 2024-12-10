def get_input_from_file(filename: str) -> list[list[int]]:
    """
    This function reads the input from a file and returns the matrix.
    """

    # Open the file
    with open(filename, "r") as file:
        # Read the lines
        lines = file.readlines()

        # Initialize the matrix
        matrix = []

        # Split the lines
        for line in lines:
            matrix.append(list(map(int, line.split(" "))))

    return matrix


def check_validity(is_increasing: bool, val1: int, val2: int) -> bool:
    """
    This function checks if the two values are valid.
    """
    if is_increasing:
        return 1 <= val2 - val1 <= 3
    else:
        return 1 <= val1 - val2 <= 3


def compute_safeness(matrix: list[list[int]]) -> int:
    """
    This function computes the similarity between two lists of integers.
    """
    # Initialize the safeness counter
    safeness = 0

    for line in matrix:
        is_valid = True
        if 1 <= abs(line[1] - line[0]) <= 3:
            is_increasing = line[1] > line[0]
            for idx in range(1, len(line) - 1):
                if not check_validity(is_increasing, line[idx], line[idx+1]):
                    is_valid = False
                    break
            if is_valid:
                safeness += 1

    # Print the safeness
    print(f"The safeness of the document is {safeness}.")
    return safeness


def compute_line_validity(line: list[int]) -> bool:
    """
    This function computes the validity of a line.
    """
    is_valid = True

    differences = [(line[idx+1] - line[idx])>0 for idx in range(0, len(line)-1)]
    if differences.count(True) > differences.count(False):
        is_increasing = True
    else:
        is_increasing = False

    for idx in range(0, len(line) - 1):
        if not check_validity(is_increasing, line[idx], line[idx+1]):
            is_valid = False
            break
    return is_valid


def compute_new_safeness(matrix: list[list[int]]) -> int:
    """
    This function computes the similarity between two lists of integers.
    """
    # Initialize the safeness counter
    safeness = 0

    for line in matrix:
        is_valid = True

        differences = [(line[idx + 1] - line[idx]) > 0 for idx in range(0, len(line) - 1)]
        if differences.count(True) > differences.count(False):
            is_increasing = True
        else:
            is_increasing = False

        for idx in range(0, len(line) - 1):
            if not check_validity(is_increasing, line[idx], line[idx+1]):
                if not compute_line_validity(line[:idx] + line[idx+1:]) and not compute_line_validity(line[:idx+1] + line[idx+2:]):
                    is_valid = False
                    break
        if is_valid:
            safeness += 1

    # Print the safeness
    print(f"The safeness of the document is {safeness}.")
    return safeness


# Ensure the main function runs only when the script is executed directly.
if __name__ == "__main__":
    # Example
    matrix_1 = [
        [7, 6, 4, 2, 1],
        [1, 2, 7, 8, 9],
        [9, 7, 6, 2, 1],
        [1, 3, 2, 4, 5],
        [8, 6, 4, 4, 1],
        [1, 3, 6, 7, 9]
    ]
    print(compute_safeness(matrix_1))

    # Real input
    matrix_1 = get_input_from_file("input.txt")
    print(compute_safeness(matrix_1))

    # Example
    matrix_1 = [
        [7, 6, 4, 2, 1],
        [1, 2, 7, 8, 9],
        [9, 7, 6, 2, 1],
        [1, 3, 2, 4, 5],
        [8, 6, 4, 4, 1],
        [1, 3, 6, 7, 9]
    ]
    print(compute_new_safeness(matrix_1))

    # Real input
    matrix_1 = get_input_from_file("input.txt")
    print(compute_new_safeness(matrix_1))
