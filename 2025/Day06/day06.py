import re


def get_input_from_file(filename: str) -> list[str]:
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

    return [line.strip('\n') for line in lines]


def _clean_operands(operands: list[str]) -> tuple[list[list[int]], list[str]]:
    """
    This function cleans the operands and returns a list of list of integers
    and the operations.

    Parameters
    ----------
    operands : list[str]
        A list of strings representing the operands and the operations to be
        performed.

    Returns
    ------
    A tuple containing:
        - A list of list of integers
        - A list of tuples representing the start and end of each range
    """

    used_operands = []

    regex_operand = r'(\d+)\s*'
    for operand in operands[:-1]:
        operand = operand.strip()
        elems = re.findall(regex_operand, operand)
        used_operands.append([int(elem) for elem in elems])

    final_operands = [
        [
            used_operands[row_idx][col_idx]
            for row_idx in range(len(used_operands))
        ]
        for col_idx in range(len(used_operands[0]))
    ]

    operations = operands[-1].strip()
    regex_operation = r'([\+\*])\s*'
    final_operations = re.findall(regex_operation, operations)

    return final_operands, final_operations


def _clean_operands_part_2(operands: list[str]) -> tuple[list[list[int]], list[str]]:
    """
    This function cleans the operands and returns a list of list of integers
    and the operations.

    Parameters
    ----------
    operands : list[str]
        A list of strings representing the operands and the operations to be
        performed.

    Returns
    ------
    A tuple containing:
        - A list of list of integers
        - A list of tuples representing the start and end of each range
    """

    final_operands = []

    HEIGHT = len(operands) - 1
    WIDTH = max(len(line) for line in operands)
    i = 0
    tmp_elems = []
    while i < WIDTH:
        j = 0
        current_elem = ''
        reset_column = True
        while j < HEIGHT:
            if i < len(operands[j]) and operands[j][i] != ' ':
                reset_column = False
                current_elem += operands[j][i]
            j += 1
        if current_elem:
            tmp_elems.append(current_elem)
        if reset_column:
            if tmp_elems:
                final_operands.append([int(elem) for elem in tmp_elems])
                tmp_elems = []
        i += 1
    if tmp_elems:
        final_operands.append([int(elem) for elem in tmp_elems])

    operations = operands[-1].strip()
    regex_operation = r'([\+\*])\s*'
    final_operations = re.findall(regex_operation, operations)

    return final_operands, final_operations


def _multiply(operands: list[int]) -> int:
    """
    This function multiplies all the integers in the list.

    Parameters
    ----------
    operands : list[int]
        A list of integers to be multiplied.

    Returns
    ------
    The product of all the integers in the list.
    """

    result = 1

    for operand in operands:
        result *= operand

    return result


def _sum(operands: list[int]) -> int:
    """
    This function sums all the integers in the list.

    Parameters
    ----------
    operands : list[int]
        A list of integers to be summed.

    Returns
    ------
    The sum of all the integers in the list.
    """

    result = 0

    for operand in operands:
        result += operand

    return result


if __name__ == "__main__":
    operands = get_input_from_file("./input.txt")

    final_operands, final_operations = _clean_operands_part_2(operands)

    res = 0
    current_idx = 0
    height = len(final_operations)

    while current_idx < height:
        operation = final_operations[current_idx]

        if operation == '+':
            res += _sum(final_operands[current_idx])
        elif operation == '*':
            res += _multiply(final_operands[current_idx])

        current_idx += 1

    print(f'Result: {res}')
