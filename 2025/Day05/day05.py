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
        lines = file.read()

    return lines.split('\n\n')


def _clean_sets(sets: str) -> list[tuple[int, int]]:
    int_sets = []
    parts = sets.split('\n')
    for p in parts:
        range_parts = p.split('-')
        start_elem = int(range_parts[0])
        end_elem = int(range_parts[1])

        int_sets.append((start_elem, end_elem))

    int_sets = sorted(int_sets, key=lambda x: x[0])
    final_sets = []

    current_start, current_end = int_sets[0]
    for start_elem, end_elem in int_sets[1:]:
        if start_elem <= current_end:
            current_end = max(current_end, end_elem)
        else:
            final_sets.append((current_start, current_end))
            current_start, current_end = start_elem, end_elem

    final_sets.append((current_start, current_end))
    return final_sets


def _clean_ids(ids: str) -> list[int]:
    id_lines = ids.split('\n')
    final_ids = [int(i) for i in id_lines]
    return sorted(final_ids)


if __name__ == "__main__":
    valid_sets, ids = get_input_from_file("./input.txt")

    final_sets = _clean_sets(valid_sets)
    ordered_ids = _clean_ids(ids)

    res = 0
    current_idx = 0

    # Part 1
    for start_elem, end_elem in final_sets:
        if current_idx >= len(ordered_ids):
            break

        while ordered_ids[current_idx] < start_elem:
            current_idx += 1
        while current_idx < len(ordered_ids) and start_elem <= ordered_ids[current_idx] <= end_elem:
            res += 1
            current_idx += 1

    print(f'Result: {res}')

    # Part 2
    res_part2 = 0

    for start_elem, end_elem in final_sets:
        res_part2 += (end_elem - start_elem + 1)

    print(f'Result Part 2: {res_part2}')
