class Button:
    x: int
    y: int
    cost: int

    def __init__(self, x: int, y: int, cost: int):
        self.x = x
        self.y = y
        self.cost = cost

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}, Cost: {self.cost}"


class Equation:
    button_a: Button
    button_b: Button
    prize: tuple[int, int]

    def __init__(self, button_a: Button, button_b: Button, prize: tuple[int, int]):
        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize

    def __str__(self):
        return f"Button A: {self.button_a}, Button B: {self.button_b}, Prize: {self.prize}"


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def build_equations(text: str) -> list[Equation]:
    equation_lists = text.split("\n\n")
    equations = []
    for eq in equation_lists:
        button_a = eq.split("\n")[0].split("A: ")[1]
        button_b = eq.split("\n")[1].split("B: ")[1]
        prize = eq.split("\n")[2].split("Prize: ")[1]
        button_a = Button(x=int(button_a.split(", ")[0].strip("X+")), y=int(button_a.split(", ")[1].strip("Y+")), cost=3)
        button_b = Button(x=int(button_b.split(", ")[0].strip("X+")), y=int(button_b.split(", ")[1].strip("Y+")), cost=1)
        prize = (int(prize.split(", ")[0].strip("X=")), int(prize.split(", ")[1].strip("Y=")))
        equations.append(Equation(button_a, button_b, prize))

    return equations


def get_fewest_tokens(text: str) -> int:
    equations = build_equations(text)

    # for eq in equations:
    #     print(eq)

    res = 0

    for eq in equations:
        counter_tokens_a = 0
        counter_tokens_b = 0
        if (eq.button_a.x + eq.button_b.x) * 100 < eq.prize[0] or (eq.button_a.y + eq.button_b.y) * 100 < eq.prize[1]:
            continue
        is_done = False
        while counter_tokens_a < 100 and not is_done:
            if (eq.prize[0] - counter_tokens_a * eq.button_a.x) % eq.button_b.x == 0:
                counter_tokens_b = (eq.prize[0] - counter_tokens_a * eq.button_a.x) // eq.button_b.x
                if counter_tokens_b < 100 and eq.prize[1] == counter_tokens_a * eq.button_a.y + counter_tokens_b * eq.button_b.y:
                    is_done = True
                else:
                    counter_tokens_a += 1
            else:
                counter_tokens_a += 1
        if is_done:
            res += counter_tokens_a * eq.button_a.cost + counter_tokens_b * eq.button_b.cost

    return res


def solve_system(ax, bx, px, ay, by, py):
    # print("System of equations:")
    # print(f"1. {a1}x + {b1}y = {c1}")
    # print(f"2. {a2}x + {b2}y = {c2}\n")

    if ax == 0:
        raise ValueError("Cannot solve for x if a1 = 0.")

    # Solve for y
    y = (py * ax - ay * px) / (by * ax - ay * bx)
    if y % 1 != 0:
        raise ValueError("No solution exists.")

    # Step 4: Substitute y back into the expression for x
    x = (px - bx * y) / ax
    if x % 1 != 0:
        raise ValueError("No solution exists.")

    return int(x), int(y)


def get_fewest_tokens_v2(text: str) -> int:
    equations = build_equations(text)

    for eq in equations:
        eq.prize = (eq.prize[0] + 10000000000000, eq.prize[1] + 10000000000000)

    res = 0
    for eq in equations:
        try:
            counter_tokens_a, counter_tokens_b = solve_system(eq.button_a.x, eq.button_b.x, eq.prize[0], eq.button_a.y, eq.button_b.y, eq.prize[1])
        except ValueError as e:
            continue
        res += counter_tokens_a * eq.button_a.cost + counter_tokens_b * eq.button_b.cost

    return res


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_fewest_tokens(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_fewest_tokens(input_text))

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    print(get_fewest_tokens_v2(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_fewest_tokens_v2(input_text))
