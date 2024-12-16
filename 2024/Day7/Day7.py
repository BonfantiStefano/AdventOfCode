import math

def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


class Equation:
    calibration_result: int
    members: list[int]

    def __init__(self, calibration_result: int, members: list[int]):
        self.calibration_result = calibration_result
        self.members = members

    def __str__(self):
        return f"Result: {self.calibration_result};\nMembers: {self.members}"


class TreeNode:
    def __init__(self, value, operation=None):
        self.value = value
        self.operation = operation
        self.left = None
        self.right = None


def build_tree(
        values: list[int],
        result: int,
        current_index=0,
        current_value=None,
) -> TreeNode | None:
    # Base case: if we've used all elements in the list, stop
    if current_index >= len(values):
        return None

    # Determine the value of the current node
    if current_value is None:
        current_value = values[current_index]

    # Create the current node
    node = TreeNode(current_value)

    # If we have more values to process, create children
    if current_index + 1 < len(values):
        next_value = values[current_index + 1]

        if current_value + next_value <= result:
            # Create left child for the + operation
            node.left = build_tree(
                values=values,
                result=result,
                current_index=current_index + 1,
                current_value=current_value + next_value
            )
            node.left.operation = "+"

        if current_value * next_value <= result:
            # Create right child for the * operation
            node.right = build_tree(
                values=values,
                result=result,
                current_index=current_index + 1,
                current_value=current_value * next_value
            )
            node.right.operation = "*"

    return node


def print_tree(node, level=0):
    if node is not None:
        print("  " * level + f"{node.value} ({node.operation or 'root'})")
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)


def check_tree(node: TreeNode, depth: int, result: int, step: int = 0) -> bool:
    if node is None:
        return False
    if step == depth-1:
        return node.value == result
    else:
        return check_tree(node.left, depth, result, step+1) or check_tree(node.right, depth, result, step+1)


def compute_calibration_result(text: str) -> int:
    # Creates the rule pairs
    equation_list = text.split("\n")
    equations = []
    for equation in equation_list:
        res, memb = equation.split(":")
        res = int(res)
        members = memb.strip(" ").split(" ")
        members = [int(member) for member in members]
        equations.append(Equation(res, members))

    # for eq in equations:
    #     print(eq)

    # Checks if the equations are valid
    res = 0

    for equation in equations:

        tree = build_tree(values=equation.members, result=equation.calibration_result)

        if check_tree(node=tree, depth=len(equation.members), result=equation.calibration_result):
            res += equation.calibration_result
    return res


class TreeNodeV2:
    def __init__(self, value, operation=None):
        self.value = value
        self.operation = operation
        self.left = None
        self.middle = None
        self.right = None


def int_concat(a: int, b: int) -> int:
    try:
        digit = math.floor(math.log10(b)) + 1
    except ValueError:
        digit = 1
    return a * 10 ** digit + b


def build_tree_v2(
        values: list[int],
        result: int,
        current_index=0,
        current_value=None,
) -> TreeNodeV2 | None:
    # Base case: if we've used all elements in the list, stop
    if current_index >= len(values):
        return None

    # Determine the value of the current node
    if current_value is None:
        current_value = values[current_index]

    # Create the current node
    node = TreeNodeV2(current_value)

    # If we have more values to process, create children
    if current_index + 1 < len(values):
        next_value = values[current_index + 1]

        if current_value + next_value <= result:
            # Create left child for the + operation
            node.left = build_tree_v2(
                values=values,
                result=result,
                current_index=current_index + 1,
                current_value=current_value + next_value
            )
            node.left.operation = "+"

        if int_concat(current_value,  next_value) <= result:
            # Create middle child for the || operation
            node.middle = build_tree_v2(
                values=values,
                result=result,
                current_index=current_index + 1,
                current_value=int_concat(current_value, next_value)
            )
            node.middle.operation = "||"

        if current_value * next_value <= result:
            # Create right child for the * operation
            node.right = build_tree_v2(
                values=values,
                result=result,
                current_index=current_index + 1,
                current_value=current_value * next_value
            )
            node.right.operation = "*"

    return node


def print_tree_v2(node, level=0):
    if node is not None:
        print("  " * level + f"{node.value} ({node.operation or 'root'})")
        print_tree_v2(node.left, level + 1)
        print_tree_v2(node.middle, level + 1)
        print_tree_v2(node.right, level + 1)


def check_tree_v2(node: TreeNodeV2, depth: int, result: int, step: int = 0) -> bool:
    if node is None:
        return False
    if step == depth-1:
        return node.value == result
    else:
        return (check_tree_v2(node.left, depth, result, step+1) or check_tree_v2(node.right, depth, result, step+1) or
                check_tree_v2(node.middle, depth, result, step+1))


def compute_calibration_result_v2(text: str) -> int:
    # Creates the rule pairs
    equation_list = text.split("\n")
    equations = []
    for equation in equation_list:
        res, memb = equation.split(":")
        res = int(res)
        members = memb.strip(" ").split(" ")
        members = [int(member) for member in members]
        equations.append(Equation(res, members))

    # Checks if the equations are valid
    res = 0

    for equation in equations:

        tree = build_tree_v2(values=equation.members, result=equation.calibration_result)
        # print_tree_v2(tree)

        if check_tree_v2(node=tree, depth=len(equation.members), result=equation.calibration_result):
            res += equation.calibration_result
    return res


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    print(compute_calibration_result(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(compute_calibration_result(input_text))

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    print(compute_calibration_result_v2(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(compute_calibration_result_v2(input_text))
