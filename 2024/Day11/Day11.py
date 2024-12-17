import math
from collections import Counter


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def get_initial_stones(text: str) -> list[int]:
    stone_list = text.split(" ")
    stones = []
    for stone in stone_list:
        stones.append(int(stone))
    return stones


def num_digits(num: int) -> int:
    return math.floor(math.log10(num)) + 1


def split_stone(stone: int) -> tuple[int, int]:
    digits = num_digits(stone)
    half = digits // 2
    first_half = stone // 10 ** half
    second_half = stone % 10 ** half
    return first_half, second_half


def recollect(stones: list[int]) -> dict[int, int]:
    stone_counts = dict(Counter(stones))
    return stone_counts


def add_value_to_dict(dictionary: dict, key: int, value: int):
    if key in dictionary:
        dictionary[key] += value
    else:
        dictionary[key] = value


def get_num_final_stones_v2(text: str) -> int:
    stones = get_initial_stones(text)
    stones = recollect(stones)

    for step in range(75):
        new_stones = {}
        for stone, value in stones.items():
            if stone == 0:
                add_value_to_dict(new_stones, 1, value)
            elif num_digits(stone) % 2 == 0:
                stone1, stone2 = split_stone(stone)
                add_value_to_dict(new_stones, stone1, value)
                add_value_to_dict(new_stones, stone2, value)
            else:
                add_value_to_dict(new_stones, stone * 2024, value)
        stones = new_stones

    return sum(stones.values())


def get_num_final_stones(text: str) -> int:
    stones = get_initial_stones(text)

    for step in range(25):
        new_stones = []
        for idx, stone in enumerate(stones):
            if stone == 0:
                new_stones.append(1)
            elif num_digits(stone) % 2 == 0:
                stone1, stone2 = split_stone(stone)
                new_stones.append(stone1)
                new_stones.append(stone2)
            else:
                new_stones.append(stone * 2024)
        stones = new_stones

    return len(stones)


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_num_final_stones(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_num_final_stones(input_text))

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_num_final_stones_v2(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_num_final_stones_v2(input_text))
