
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


def read_files():
    # Load the word list, and the letter and digraph frequencies
    with open('dict.txt', 'r') as f:
        common_words_set = set(line.strip() for line in f)

    # Create a dictionary where the key is the lowercase letter and the value is the frequency as a float.
    with open('Letter_Freq.txt', 'r') as f:
        letter_freqs = {line.strip().split('\t')[1].lower(): float(line.strip().split('\t')[0]) for line in f}

    # a dictionary mapping lowercase letter pairs to their frequencies
    # the key is the letters pair and the value is the frequency as a float.
    with open('Letter2_Freq.txt', 'r') as f:
        letters_pair_freq = {}
        for line in f:
            # only proccess lines that contain a tab character
            if "\t" in line:
                letters_pair_freq[line.strip().split('\t')[1].lower()] = float(line.strip().split('\t')[0])
                # last line in file should be for "ZZ"
                if line.strip().split('\t')[1].lower() == "zz":
                    break
    return common_words_set, letter_freqs, letters_pair_freq


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
    # print(perm)
    find_and_replace(perm[0], "enc.txt", "output.txt")
    read_files()

