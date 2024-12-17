def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def correct_order_v2(rules: str, updates: str) -> int:
    # Creates the rule pairs
    rules = rules.split("\n")
    rules_pair = []
    for rule in rules:
        fst, snd = rule.split("|")
        rules_pair.append((int(fst), int(snd)))

    # Creates the updates list
    updates = updates.split("\n")
    updates_list = []
    for update in updates:
        new_list = []
        numbers = update.split(",")
        for number in numbers:
            new_list.append(int(number))
        updates_list.append(new_list)

    # Create a dependence structure with the rules, where each pair is a relationship between the two numbers,
    # the first number must be before the second number in the heap (so closer to the top)
    dependencies = {}
    for pair in rules_pair:
        if pair[0] not in dependencies:
            dependencies[pair[0]] = []
        dependencies[pair[0]].append(pair[1])
    print(dependencies)

    # Checks if the updates are valid
    res = 0

    for update in updates_list:
        is_valid = True
        for idx, elem in enumerate(update[:-1]):
            if is_valid and update[idx] in dependencies:
                for val in update[idx+1:]:
                    if val not in dependencies[update[idx]]:
                        is_valid = False
                        break
            else:
                is_valid = False
                break
        if not is_valid:
            corrected_update = correct_list(update, dependencies)
            res += corrected_update[len(corrected_update)//2]

    return res


def correct_list(update, dependencies):
    final_list = update.copy()
    for elem in update:
        try:
            contained_elems = [other_elem for other_elem in update if other_elem in dependencies[elem]]
            final_list[len(update) - len(contained_elems) - 1] = elem
        except KeyError:
            final_list[len(update) - 1] = elem
    return final_list


def correct_order(rules: str, updates: str) -> int:
    # Creates the rule pairs
    rules = rules.split("\n")
    rules_pair = []
    for rule in rules:
        fst, snd = rule.split("|")
        rules_pair.append((int(fst), int(snd)))

    # Creates the updates list
    updates = updates.split("\n")
    updates_list = []
    for update in updates:
        new_list = []
        numbers = update.split(",")
        for number in numbers:
            new_list.append(int(number))
        updates_list.append(new_list)

    # Create a dependence structure with the rules, where each pair is a relationship between the two numbers,
    # the first number must be before the second number in the heap (so closer to the top)
    dependencies = {}
    for pair in rules_pair:
        if pair[0] not in dependencies:
            dependencies[pair[0]] = []
        dependencies[pair[0]].append(pair[1])

    # Checks if the updates are valid
    res = 0

    for update in updates_list:
        is_valid = True
        for idx, elem in enumerate(update[:-1]):
            if is_valid and update[idx] in dependencies:
                for val in update[idx+1:]:
                    if val not in dependencies[update[idx]]:
                        is_valid = False
                        break
            else:
                is_valid = False
                break
        if is_valid:
            res += update[len(update)//2]

    return res


if __name__ == "__main__":
    # Example
    text = get_input_from_file("example.txt")
    rules_ex, updates_ex = text.split("\n\n")
    print(correct_order(rules_ex, updates_ex))

    # Real input
    text = get_input_from_file("input.txt")
    rules_in, updates_in = text.split("\n\n")
    print(correct_order(rules_in, updates_in))

    # Part 2
    # Example
    text = get_input_from_file("example.txt")
    rules_ex, updates_ex = text.split("\n\n")
    print(correct_order_v2(rules_ex, updates_ex))

    # Real input
    text = get_input_from_file("input.txt")
    rules_in, updates_in = text.split("\n\n")
    print(correct_order_v2(rules_in, updates_in))
