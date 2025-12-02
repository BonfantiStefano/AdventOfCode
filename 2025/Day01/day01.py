START_VALUE = 50
TOTAL_VALUES = 100


def _parse_rotation(rotation: str) -> int:
    """
    This function parses a rotation string and returns the corresponding integer value.

    Parameters
    ----------
    rotation : str
        The rotation string to be parsed

    Returns
    -------
    The integer value of the rotation
    """

    direction = rotation[0]
    magnitude = int(rotation[1:])

    if direction == "R":
        return magnitude
    elif direction == "L":
        return -magnitude
    else:
        raise ValueError(f"Invalid rotation direction: {direction}")


def _clear_rotation_number(rotation_number: int, password_counter: int) -> tuple[int, int]:
    """
    This function clears the rotation number to be within the valid range.

    :param rotation_number: The rotation number to be cleared
    :param password_counter: The current password counter
    :return: The cleared rotation number and the updated password counter
    """
    abs_rotation = abs(rotation_number)

    if abs_rotation >= TOTAL_VALUES:
        times = abs_rotation // TOTAL_VALUES
        password_counter += times
        rotation_number = rotation_number - (times * TOTAL_VALUES * (1 if rotation_number > 0 else -1))
        print(f'Cleared rotation number to {rotation_number}, updated password counter to {password_counter}')
    return rotation_number, password_counter


def handle_rotation(start_value: int, rotation: str, password_counter: int) -> tuple[int, int]:
    """
    This function handles a single rotation and returns the new value.

    Parameters
    ----------
    start_value : int
        The initial value before the rotation
    rotation : str
        The rotation to be applied
    password_counter : int
        The counter for the password

    Returns
    -------
    The new value after the rotation and the updated password counter
    """
    print(f'Handling rotation {rotation} from starting value {start_value}')
    rotation_number = _parse_rotation(rotation)

    rotation_number, password_counter = _clear_rotation_number(rotation_number, password_counter)

    new_value = (start_value + rotation_number) % TOTAL_VALUES
    print(f'Reached value: {new_value}')

    if start_value != 0 and (start_value + rotation_number >= TOTAL_VALUES or start_value + rotation_number <= 0):
        password_counter += 1
        print(f'Updated password counter to {password_counter}')

    return new_value, password_counter


def get_input_from_file(filename: str) -> list[str]:
    """
    This function reads the input from a file and return the list of rotations.

    Returns
    ------
    A list of rotations
    """

    # Open the file
    with open(filename, "r") as file:
        # Read the lines
        lines = file.readlines()

    return [line.strip() for line in lines]


if __name__ == "__main__":
    # Get the input from the file
    rotations = get_input_from_file("./input.txt")
    password_counter = 0
    initial_value = START_VALUE
    print(f'Starting from {initial_value}')

    for rotation in rotations:
        initial_value, password_counter = handle_rotation(initial_value, rotation, password_counter)

    print(f"The password is {password_counter}.")