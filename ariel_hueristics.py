import collections
import string
import itertools

from main import read_files

""" heuristic 2:
    for each permutation, compute the frequencies of each letter on our decrypted output text,
    and compare that frequency to the known frequency of the letter which is in the given file "Letter_Freq".

"""


# TODO what if a letter isnt in the file? still should be a key and get freq 0!
def compute_perm_letter_freq(filename):
    with open(filename, 'r') as f:
        content = f.read().lower()
    # Create a counter for letters in the content
    letter_counter = collections.Counter(c for c in content if c in string.ascii_lowercase)
    # Calculate total number of letters in file
    total_letters = sum(letter_counter.values())
    # Calculate frequencies and store them in a dictionary
    perm_letter_freqs = {letter: count / total_letters for letter, count in letter_counter.items()}
    return perm_letter_freqs


# compare current perm frequencies wit known frequencies
def compare_freqs(perm_letter_freqs, known_letter_freqs):
    total_difference = 0
    for letter in string.ascii_lowercase:
        # Get the frequency of the letter in perm_letter_freqs, or 0 if the letter isn't present
        # TODO delete the 0 option after making sure each letter in dict even when 0 occurrences
        perm_freq = perm_letter_freqs.get(letter, 0)
        # Get the frequency of the letter in known_letter_freqs, or 0 if the letter isn't present
        known_freq = known_letter_freqs.get(letter, 0)

        # Add the absolute difference between the frequencies to the total difference
        total_difference += abs(perm_freq - known_freq)

    return total_difference


def compute_letter_pairs_freq(filename, known_letter_pairs_freqs):
    # Copy the keys from known_letter_pairs_freqs and initialize pair_counter with them
    pair_counter = collections.Counter(dict.fromkeys(known_letter_pairs_freqs.keys(), 0))

    with open(filename, 'r') as f:
        content = f.read().lower()

    # Count occurrences of each pair in the content
    for i in range(len(content) - 1):
        pair = content[i:i + 2]
        if pair in pair_counter:
            pair_counter[pair] += 1

    # Calculate total number of pairs
    total_pairs = sum(pair_counter.values())
    # Calculate frequencies and store them in a dictionary
    pair_freqs = {pair: count / total_pairs for pair, count in pair_counter.items()}

    return pair_freqs


def compare_pairs_freqs(pair_freqs, known_letter_pairs_freqs):
    total_difference = 0

    # Iterate over each pair in known_letter_pairs_freqs
    for pair in known_letter_pairs_freqs.keys():
        # Get the frequency of the pair in pair_freqs
        perm_pairs_freq = pair_freqs[pair]
        # Get the frequency of the pair in known_letter_pairs_freqs
        known_pairs_freq = known_letter_pairs_freqs[pair]
        # Add the absolute difference between the frequencies to the total difference
        total_difference += abs(perm_pairs_freq - known_pairs_freq)

    return total_difference


if __name__ == '__main__':
    perm_letter_freqs = compute_perm_letter_freq('output.txt')
    # for letter, freq in sorted(perm_letter_freqs.items()):
    #     print(f'{letter}: {freq:.4f}')

    common_words_set, known_letter_freqs, known_letter_pairs_freqs = read_files()
    compare_freqs(perm_letter_freqs, known_letter_freqs)
    difference = compare_freqs(perm_letter_freqs, known_letter_freqs)
    print(f'letters freq Total difference: {difference:.4f}')

    pair_freqs = compute_letter_pairs_freq('output.txt', known_letter_pairs_freqs)
    # for pair, freq in sorted(pair_freqs.items()):
    #     print(f'{pair}: {freq:.4f}')

    difference = compare_pairs_freqs(pair_freqs, known_letter_pairs_freqs)
    print(f'pairs freq Total difference: {difference:.4f}')
