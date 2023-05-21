import random
import string

common_words_set = set()
letter_freqs = {}
letters_pair_freq = {}




def crossover(p1, p2):
    crossover_point = random.randint(0, len(p1))
    child1 = {}
    child2 = {}
    for i in range(crossover_point):
        key1, value1 = list(p1.items())[i]
        key2, value2 = list(p2.items())[i]
        child1[key1] = value1
        child2[key2] = value2

    for i in range(crossover_point, len(p1)):
        key1, value1 = list(p1.items())[i]
        key2, value2 = list(p2.items())[i]
        child1[key2] = value2
        child2[key1] = value1
    check_duplicates(child1)
    check_duplicates(child2)
    return child1, child2


def check_duplicates(dictionary):
    values = set()
    duplicates = set()
    for value in dictionary.values():
        if value in values:
            duplicates.add(value)
        values.add(value)

    if duplicates:
        unused_letters = list(set(string.ascii_uppercase) - set(dictionary.values()))
        for key, value in dictionary.items():
            if value in duplicates:
                dictionary[key] = get_unique_value(values, unused_letters)

def get_unique_value(values, unused_letters):
    while True:
        unique_value = random.choice(unused_letters)
        if unique_value not in values:
            return unique_value

def perform_mutation(dictionary):
    keys = list(dictionary.keys())
    # TODO: necessary?
    if len(keys) < 2:
        return
    key1, key2 = random.sample(keys, 2)
    value1 = dictionary[key1]
    value2 = dictionary[key2]
    dictionary[key1] = value2
    dictionary[key2] = value1


if __name__ == '__main__':
    perm = generate_permutations(10)
    read_files()
    final_scores = []
    for dicti in perm:
        find_and_replace(dicti, "enc.txt", "output.txt")
        final_scores.append(search_common_words("output.txt"))
    print(final_scores)

