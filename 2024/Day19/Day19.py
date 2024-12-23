def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def build_towels_patterns(text: str) -> tuple[list[str], list[str]]:
    towel_list, pattern_list = text.split("\n\n")

    return towel_list.split(", "), pattern_list.split("\n")


def analyze_pattern(pattern: str, towels: list[str]) -> bool:
    if not pattern:
        return True

    for towel in towels:
        if pattern.startswith(towel):
            is_possible = analyze_pattern(pattern[len(towel):], towels)
            if is_possible:
                return True

    return False


def get_possible_patterns(text: str) -> tuple[int, list[str]]:
    towels, patterns = build_towels_patterns(text)

    res = []
    for pattern in patterns:
        for towel in towels:
            if pattern.startswith(towel):
                is_possible = analyze_pattern(pattern[len(towel):], towels)
                if is_possible:
                    res.append(pattern)
                    break

    return len(res), res


def analyze_pattern_v2(pattern: str, towels: list[str], cache: dict[str, int]) -> int:
    if not pattern:
        return 1

    if pattern in cache:
        return cache[pattern]

    res = 0
    for towel in towels:
        if pattern.startswith(towel):
            res += analyze_pattern_v2(pattern[len(towel):], towels, cache)

    cache[pattern] = res
    return res


def get_possible_patterns_v2(text: str) -> int:
    towels, patterns = build_towels_patterns(text)

    res = 0
    cache = {}
    for pattern in patterns:
        res += analyze_pattern_v2(pattern, towels, cache)

    return res


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_possible_patterns(input_text)[0])

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_possible_patterns(input_text)[0])

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_possible_patterns_v2(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_possible_patterns_v2(input_text))
