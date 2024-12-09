def compute_similarity(list1: list[int], list2: list[int]) -> int:
    """
    This function computes the similarity between two lists of integers.
    """
    # Initialize the similarity counter
    similarity = 0

    # Sort the lists
    list1.sort()
    list2.sort()

    # Iterate over the two lists
    for i in range(len(list1)):
        if list1[i] >= list2[i]:
            similarity += list1[i] - list2[i]
        else:
            similarity += list2[i] - list1[i]

    # Print the similarity
    print(f"The similarity between the two lists is {similarity}.")
    return similarity


def get_input_from_file(filename: str) -> tuple[list[int], list[int]]:
    """
    This function reads the input from a file and returns the two lists.
    """

    # Open the file
    with open(filename, "r") as file:
        # Read the lines
        lines = file.readlines()

        list1 = [None] * len(lines)
        list2 = [None] * len(lines)

        # Split the lines
        for idx, line in enumerate(lines):
            val1, val2 = line.strip().split("   ")
            list1[idx] = int(val1)
            list2[idx] = int(val2)

    return list1, list2


def compute_new_similarity(list1: list[int], list2: list[int]) -> int:
    """
    This function computes the similarity between two lists of integers.
    """
    # Initialize the similarity counter
    similarity = 0

    # Compute the frequency of each element in the two lists
    freq1 = {}
    freq2 = {}

    for i in range(len(list1)):
        freq1[list1[i]] = freq1.get(list1[i], 0) + 1
        freq2[list2[i]] = freq2.get(list2[i], 0) + 1

    for key in freq1.keys():
        if key in freq2.keys():
            similarity += key * freq2[key] * freq1[key]

    # Print the similarity
    print(f"The similarity between the two lists is {similarity}.")
    return similarity


# Ensure the main function runs only when the script is executed directly.
if __name__ == "__main__":
    # Example
    list_1 = [3, 4, 2, 1, 3, 3]
    list_2 = [4, 3, 5, 3, 9, 3]
    print(compute_similarity(list_1, list_2))

    # Real input
    list_1, list_2 = get_input_from_file("input.txt")
    print(compute_similarity(list_1, list_2))

    # Example
    list_1 = [3, 4, 2, 1, 3, 3]
    list_2 = [4, 3, 5, 3, 9, 3]
    print(compute_new_similarity(list_1, list_2))

    # Real input
    list_1, list_2 = get_input_from_file("input.txt")
    print(compute_new_similarity(list_1, list_2))
