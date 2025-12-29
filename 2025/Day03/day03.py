LEN_BATTERY = 12


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


def _find_highest_voltage(num: str) -> int:
    """
    Find the highest voltage in the given battery

    :param num: The battery to be checked
    :return: The highest voltage found
    """

    if len(num) < 2:
        return 0
    if len(num) == 2:
        return int(num)

    first_value = int(num[0])
    second_value = int(num[1])
    idx = 2
    while idx < len(num):
        current_value = int(num[idx])
        if current_value > second_value and current_value <= first_value:
            second_value = current_value
        elif current_value > first_value:
            if idx + 1 < len(num):
                first_value = current_value
                second_value = 0
            else:
                second_value = current_value
        idx += 1

    # print(f'For battery {num}, found highest voltage {first_value}{second_value}')
    return int(first_value) * 10 + int(second_value)


def _find_highest_voltage_part_2(num: str) -> int:
    """
    Find the highest voltage in the given battery

    :param num: The battery to be checked
    :return: The highest voltage found
    """

    if len(num) < LEN_BATTERY:
        return 0
    if len(num) == LEN_BATTERY:
        return int(num)

    actual_value = num[0] + '0' * (LEN_BATTERY - 1)
    idx = 1
    while idx < len(num):
        current_value = num[idx]
        if current_value < actual_value[-1]:
            idx += 1
            continue
        base_idx = max(0, LEN_BATTERY - (len(num) - idx))
        while base_idx < LEN_BATTERY:
            if current_value > actual_value[base_idx]:
                actual_value = actual_value[:base_idx] + current_value + '0' * (LEN_BATTERY - base_idx - 1)
                break
            base_idx += 1
        idx += 1

    print(f'For battery {num}, found highest voltage {actual_value}')
    return int(actual_value)


def _find_highest_voltage_not_efficient(num: str) -> int:
    """
    Find the highest voltage in the given battery

    :param num: The battery to be checked
    :return: The highest voltage found
    """

    first_value = max(num[:-1])
    idx_first = num.index(first_value)
    second_value = max(num[idx_first + 1:])
    print(f'For battery {num}, found highest voltage {first_value}{second_value}')
    return int(first_value) * 10 + int(second_value)


if __name__ == "__main__":
    input_data = get_input_from_file("./input.txt")

    res = 0
    for battery in input_data:
        res += _find_highest_voltage_part_2(battery)

    print(res)
