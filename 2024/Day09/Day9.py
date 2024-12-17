import copy


class Document:
    def __init__(self, id: int, size: int):
        self.id = id
        self.size = size

    def __str__(self):
        return f"Document {self.id} with size {self.size}"


def get_input_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def realloc_space(text: str) -> int:
    res = 0

    if len(text) % 2 == 0:
        text = text[:-1]

    files = []
    for i in range(0, len(text), 2):
        files.append(Document(id=i//2, size=int(text[i])))

    tot_length = sum([file.size for file in files])
    i = 0
    new_text = []
    while len(new_text) < tot_length:
        if i % 2 == 0:
            new_text += [files[0].id] * files[0].size
            files.pop(0)
        else:
            counter = int(text[i])
            while counter > 0:
                new_elem = min(files[-1].size, counter)
                new_text += [files[-1].id] * new_elem
                counter -= new_elem
                if new_elem == files[-1].size:
                    files.pop()
                    if len(files) == 0:
                        break
                else:
                    files[-1].size -= new_elem

        i += 1

    for idx, elem in enumerate(new_text):
        res += elem * idx
    return res


def realloc_space_v2(text: str) -> int:
    res = 0

    if len(text) % 2 == 0:
        text = text[:-1]

    files = []
    for i in range(0, len(text), 2):
        files.append(Document(id=i//2, size=int(text[i])))

    i = 0
    new_text = []
    new_files = copy.deepcopy(files)
    while new_files:
        # if len(files) == 3:
        #     print("3 files left")
        if i % 2 == 0:
            if i // 2 == new_files[0].id:
                new_text += [new_files[0].id] * new_files[0].size
                new_files.pop(0)
            else:
                new_text += [0] * files[i//2].size
        else:
            counter = int(text[i])
            for idx in range(len(new_files), 0, -1):
                if new_files[idx-1].size <= counter:
                    new_text += [new_files[idx-1].id] * new_files[idx-1].size
                    counter -= new_files[idx-1].size
                    new_files.pop(idx-1)
                    if counter == 0:
                        break
            if counter > 0:
                new_text += [0] * counter

        i += 1

    for idx, elem in enumerate(new_text):
        res += elem * idx
    return res


if __name__ == "__main__":
    # Example
    input_text = get_input_from_file("example.txt")
    print(realloc_space(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(realloc_space(input_text))

    # Part 2
    # Example
    input_text = get_input_from_file("example.txt")
    print(realloc_space_v2(input_text))

    # Real input
    input_text = get_input_from_file("input.txt")
    print(realloc_space_v2(input_text))
