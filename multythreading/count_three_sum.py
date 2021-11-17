def read_ints(path):
    lst = []
    with open(path, "r") as file:
        while line := file.readline():
            lst.append(int(line))
    return lst


def count_three_sum(ints, thread_name='t'):
    print(f'started count_three_sum in {thread_name}')
    n = len(ints)

    counter = 0

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if ints[i] + ints[j] + ints[k] == 0:
                    counter += 1
                    print(f"triple found in {thread_name}: {ints[i]}, {ints[j]}, {ints[k]}", end="\n")  # можно убрать эту строчку

    print(f'finished count_three_sum in {thread_name}. Triplets amount is {counter}')
    return counter
