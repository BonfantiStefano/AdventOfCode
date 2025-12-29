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

    return [line.strip() for line in lines]


def _check_valid_id(num: str) -> bool:
    """
    This function checks if the given id is valid.

    :param num: The id to be checked
    :return: A boolean indicating if the id is valid
    """

    if len(num) % 2 != 0:
        return False

    half_len = len(num) // 2
    part1 = num[:half_len]
    part2 = num[half_len:]

    if part1 == part2:
        return True
    return False


def _check_valid_id2(num: str) -> bool:
    """
    This function checks if the given id is valid.

    :param num: The id to be checked
    :return: A boolean indicating if the id is valid
    """

    idx = 1
    base_idx = 1
    acc = num[0:base_idx]
    while base_idx <= len(num) // 2:
        if idx + len(acc) > len(num):
            base_idx += 1
        new_part = num[idx:idx+len(acc)]
        if new_part == acc:
            idx += len(acc)
            if idx == len(num):
                return True
        else:
            base_idx += 1
            acc = num[0:base_idx]
            idx = base_idx
    return False


if __name__ == "__main__":
    input_data = get_input_from_file("./input.txt")[0]
    parts = input_data.split(",")

    res = 0
    for part in parts:
        num1, num2 = part.split("-")
        for i in range(int(num1), int(num2)+1):
            if _check_valid_id2(str(i)):
                res += i

    print(res)
