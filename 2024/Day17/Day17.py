import z3

def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def build_regs_and_operations(text: str) -> tuple[dict[str, int], list[int]]:
    reg_list, operation_list = text.split("\n\n")

    reg_list = reg_list.split("\n")
    regs = {}
    for reg in reg_list:
        reg_key = reg.split("Register ")[1].split(": ")[0]
        reg_value = int(reg.split(": ")[1])
        regs[reg_key] = reg_value

    operation_list = operation_list.split(": ")[1].split(",")
    operations = []
    for op in operation_list:
        operations.append(int(op))

    return regs, operations


def compute_final_res(nums: list[int]) -> str:
    final_str = ""
    for num in nums[:-1]:
        final_str += str(num) + ","
    final_str += str(nums[-1])
    return final_str


def perform_operation(registers: dict[str, int], input_value: int, operation: int, instruction_pointer: int) -> tuple[int, int]:
    res = 0
    is_valid_jump = False
    match operation:
        case 0:
            registers['A'] = registers['A'] // (2 ** input_value)
        case 1:
            registers['B'] = registers['B'] ^ input_value
        case 2:
            registers['B'] = input_value % 8
        case 3:
            if registers['A'] != 0:
                is_valid_jump = True
        case 4:
            registers['B'] = registers['B'] ^ registers['C']
        case 5:
            res = input_value % 8
        case 6:
            registers['B'] = registers['A'] // (2 ** input_value)
        case 7:
            registers['C'] = registers['A'] // (2 ** input_value)
        case _:
            raise ValueError(f"Operation {operation} not found")

    if is_valid_jump:
        instruction_pointer = input_value
    else:
        instruction_pointer += 2

    return res, instruction_pointer


def get_right_input_value(val: int, registers: dict[str, int | z3.ArithRef], operator: int) -> int:
    combo_ops = [0, 2, 5, 6, 7]
    if val == 4 and operator in combo_ops:
        return registers['A']
    elif val == 5 and operator in combo_ops:
        return registers['B']
    elif val == 6 and operator in combo_ops:
        return registers['C']
    elif (val >= 7 or val < 0) and operator in combo_ops:
        raise ValueError(f"Combo {val} not found")
    return val


def get_final_result(text: str) -> str:
    registers, operations = build_regs_and_operations(text)

    instruction_pointer = 0
    output = []
    counter = 0

    while instruction_pointer < len(operations):
        counter += 1
        operation = operations[instruction_pointer]
        val = operations[instruction_pointer + 1]

        input_value = get_right_input_value(val, registers, operation)

        print(f"Counter: {counter},\nOperation: {operation},\nInput: {input_value},\nRegisters: {registers}")

        res, instruction_pointer = perform_operation(
            operation=operation,
            input_value=input_value,
            registers=registers,
            instruction_pointer=instruction_pointer,
        )

        if operation == 5:
            output.append(res)
            print(f"Output: {res}")
        print("")

    final_str = "No result"
    if len(output) > 0:
        final_str = compute_final_res(output)
    print(registers)

    return final_str


def perform_operation_v2(registers, input_value, operation, instruction_pointer, counter, max_counter):
    res = z3.BitVec('res', 48)
    is_valid_jump = False
    match operation:
        case 0:
            registers['A'] = registers['A'] >> input_value
        case 1:
            registers['B'] = registers['B'] ^ input_value
        case 2:
            registers['B'] = input_value & 7
        case 3:
            if counter < max_counter:
                is_valid_jump = True
        case 4:
            registers['B'] = registers['B'] ^ registers['C']
        case 5:
            res = input_value & 7
        case 6:
            registers['B'] = registers['A'] >> input_value
        case 7:
            registers['C'] = registers['A'] >> input_value
        case _:
            raise ValueError(f"Operation {operation} not found")

    if is_valid_jump:
        instruction_pointer = input_value.as_long()
    else:
        instruction_pointer += 2

    return res, instruction_pointer


def get_input_value_a(text: str) -> int:
    solver = z3.Optimize()
    register_a = z3.BitVec('A', 48)
    registers, operations = build_regs_and_operations(text)
    registers['A'] = register_a
    registers['B'] = z3.BitVecVal(registers['B'], 48)
    registers['C'] = z3.BitVecVal(registers['C'], 48)

    instruction_pointer = 0
    output = []

    while instruction_pointer < len(operations):
        operation = operations[instruction_pointer]
        val = operations[instruction_pointer + 1]

        input_value = get_right_input_value(val, registers, operation)
        if isinstance(input_value, int):
            input_value = z3.BitVecVal(input_value, 48)

        res, instruction_pointer = perform_operation_v2(
            operation=operation,
            input_value=input_value,
            registers=registers,
            instruction_pointer=instruction_pointer,
            counter=len(output),
            max_counter=len(operations),
        )

        if operation == 5:
            output.append(res)
            solver.add(operations[len(output)-1] == res)

    solver.minimize(register_a)
    assert str(solver.check()) == 'sat'
    final_res = solver.model().eval(register_a)

    return final_res.as_long()


if __name__ == "__main__":
    # # Example
    # input_text = get_input_from_file("example.txt")
    # print(get_final_result(input_text))

    # # Example 2
    # input_text = get_input_from_file("example2.txt")
    # print(get_final_result(input_text))

    # # Real input
    # input_text = get_input_from_file("input.txt")
    # print(get_final_result(input_text))

    # # Part 2
    # # Example
    # input_text = get_input_from_file("example.txt")
    # print(get_input_value_a(input_text))

    # # Example 2
    # input_text = get_input_from_file("example2.txt")
    # print(get_input_value_a(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(get_input_value_a(input_text))
