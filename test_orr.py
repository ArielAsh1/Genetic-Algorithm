# ex2
# checkww

import random
import string

def find_and_replace(permutation, input_file, output_file):
    with open(input_file, 'r') as file_in, open(output_file, 'w') as file_out:
        for line in file_in:
            converted_line = ''
            for char in line:
                if char.isalpha() and char.lower() in permutation:
                    converted_char = permutation[char.lower()]
                    if char.isupper():
                        converted_char = converted_char.upper()
                    converted_line += converted_char
                else:
                    converted_line += char
            file_out.write(converted_line)


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
    find_and_replace(perm[0], "enc.txt", "output.txt")

