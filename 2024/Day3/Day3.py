import re


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def clear_formula(formula: str) -> int:
    """
    This function clears the formula from the unwanted characters.
    """
    res = 0
    mul_regex = r'mul\((\d+),(\d+)\)'
    pairs = re.findall(mul_regex, formula)

    for pair in pairs:
        res += int(pair[0]) * int(pair[1])
    return res


def clear_formula_v2(formula: str) -> int:
    """
    This function clears the formula from the unwanted characters.
    """
    res = 0
    mul_regex = r'mul\((\d+),(\d+)\)'
    dict_to_find = {
        0: 'do()',
        1: 'don\'t()',
    }
    actual = 1

    idx_change = formula.find(dict_to_find[actual])
    while idx_change != -1:
        to_analyze = formula[:idx_change]
        formula = formula[idx_change + len(dict_to_find[actual]):]
        if actual == 1:
            pairs = re.findall(mul_regex, to_analyze)
            for pair in pairs:
                res += int(pair[0]) * int(pair[1])

        actual = 1 ^ actual
        idx_change = formula.find(dict_to_find[actual])

    if actual == 1:
        pairs = re.findall(mul_regex, formula)
        for pair in pairs:
            res += int(pair[0]) * int(pair[1])
    return res


if __name__ == "__main__":
    # Example
    form = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
    print(clear_formula(form))

    # Real input
    form = get_input_from_file("input.txt")
    print(clear_formula(form))

    # Part 2
    # Example
    form = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    print(clear_formula_v2(form))

    # Real input
    form = get_input_from_file("input.txt")
    print(clear_formula_v2(form))
