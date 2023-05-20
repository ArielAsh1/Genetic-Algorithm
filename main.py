# ex2

import random
import string

def read_files():
    # Load the word list, and the letter and digraph frequencies
    with open('dict.txt', 'r') as f:
        word_list = set(line.strip() for line in f)
        # print(word_list)

    # Create a dictionary where the key is the lowercase letter and the value is the frequency as a float.
    with open('Letter_Freq.txt', 'r') as f:
        letter_freqs = {line.strip().split('\t')[1].lower(): float(line.strip().split('\t')[0]) for line in f}
        # print((letter_freqs))

    # a dictionary mapping lowercase letter pairs to their frequencies
    # the key is the letters pair and the value is the frequency as a float.
    with open('Letter2_Freq.txt', 'r') as f:
        digraph_freqs = {}
        for line in f:
            # only proccess lines that contain a tab character
            if "\t" in line:
                print(line)
                digraph_freqs[line.strip().split('\t')[1].lower()] = float(line.strip().split('\t')[0])
        print(digraph_freqs)

def generate_permutations(starting_population):
    alphabet = list(string.ascii_lowercase)
    permutations = []

    for _ in range(starting_population):
        random.shuffle(alphabet)
        permutation = {letter: substitute for letter, substitute in zip(string.ascii_lowercase, alphabet)}
        permutations.append(permutation)

    return permutations


if __name__ == '__main__':
    read_files()
    # perm = generate_permutations(10)
    # for x in perm:
    #     print(x)
