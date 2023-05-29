import collections
import string

COMMON_WEIGHT = 1.5
IMPORTANT_WEIGHT = 2.5


def compute_perm_letter_freq(filename, known_letter_freqs):
    """ for each permutation, compute the frequencies of each letter on our deciphered output text,
        and compare that frequency to the known frequency of the letter, which is in the given file "Letter_Freq".
    """
    # a dict to count occurrences of each letter (keys copied from known_letter_freqs)
    letter_counter = collections.Counter(dict.fromkeys(known_letter_freqs.keys(), 0))
    with open(filename, 'r') as f:
        deciphered_file = f.read().lower()
    # Count occurrences of each letter in the deciphered_file
    for letter in deciphered_file:
        if letter in letter_counter:
            letter_counter[letter] += 1

    total_letters = sum(letter_counter.values())
    # Calculate frequencies and store them in dict
    perm_letter_freqs = {letter: count / total_letters for letter, count in letter_counter.items()}
    return perm_letter_freqs


# compare current perm frequencies with the known frequencies
def compare_letter_freqs(perm_letter_freqs, known_letter_freqs):
    total_difference = 0
    for letter in string.ascii_lowercase:
        # Get the frequency of the letter in perm_letter_freqs
        perm_freq = perm_letter_freqs[letter]
        # Get the frequency of the letter in known_letter_freqs
        known_freq = known_letter_freqs[letter]
        # Add the absolute difference between the frequencies to the total difference
        total_difference += abs(perm_freq - known_freq)

    return total_difference


def compute_letter_pairs_freq(filename, known_letter_pairs_freqs):
    """ for each permutation, compute the frequencies of each letter pair on our deciphered output text,
        and compare that frequency to the known frequency of the pair, which is in the given file "Letter_Freq2".
    """
    # Copy the keys from known_letter_pairs_freqs and initialize pair_counter with them
    pair_counter = collections.Counter(dict.fromkeys(known_letter_pairs_freqs.keys(), 0))
    with open(filename, 'r') as f:
        deciphered_file = f.read().lower()
    # Run through all pairs in the file and count their occurrences
    for i in range(len(deciphered_file) - 1):
        pair = deciphered_file[i:i + 2]
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


def get_common_words_score(perm_deciphered_file, common_words):
    """ iterates over the words in the deciphered output text file of current perm,
        and searches for matches with the words in the given common_words.
        it also tries to match some specified important words.
        It then assigns specific scores based on the frequency of these words.
    """
    perm_words_score = 0
    common_words_found = 0
    important_words_found = 0
    output_word_count = 0
    important_words = {"i", "a"}

    with open(perm_deciphered_file, "r") as deciphered_file:
        for line in deciphered_file:
            words = line.split()
            output_word_count += len(words)
            for word in words:
                if word.isalpha():
                    if word.lower() in common_words:
                        common_words_found += 1
                    elif word.lower in important_words:
                        important_words_found += 1
        # Calculate the score (and avoid division by zero)
    if output_word_count != 0:
        perm_words_score = (common_words_found * COMMON_WEIGHT +
                            important_words_found * IMPORTANT_WEIGHT) / output_word_count
    return perm_words_score

