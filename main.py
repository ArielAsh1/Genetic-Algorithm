# ex2
# checkww

import random
import string


def generate_permutations(starting_population):
    alphabet = list(string.ascii_lowercase)
    permutations = []

    for _ in range(starting_population):
        random.shuffle(alphabet)
        permutation = {letter: substitute for letter, substitute in zip(string.ascii_lowercase, alphabet)}
        permutations.append(permutation)

    return permutations


if __name__ == '__main__':
    perm = generate_permutations(10)
    for x in perm:
        print(x)
