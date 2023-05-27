import collections
import string

from main import COMMON_WEIGHT, IMPORTANT_WEIGHT

# TODO: remove as well
COMMON_WORDS_SCORE = 10
IMPORTANT_WORDS_SCORE = 25

def get_letter_score(filename, known_letter_freqs):
    """ count the occurrences of each letter on our deciphered output text, and multiply that count with
        the known frequency of that letter, which is given in the "Letter_Freq" file.
    """
    # a dict to count occurrences of each letter (keys copied from known_letter_freqs)
    letter_counter = collections.Counter(dict.fromkeys(known_letter_freqs.keys(), 0))
    with open(filename, 'r') as f:
        deciphered_file = f.read().lower()
    # Count occurrences of each letter in the deciphered_file
    for letter in deciphered_file:
        if letter in letter_counter:
            letter_counter[letter] += 1

    # Multiply the count of each letter by the known frequency of that letter
    letter_scores = {letter: count * known_letter_freqs[letter] for letter, count in letter_counter.items()}
    # Sum up the scores to get the total score
    total_score = sum(letter_scores.values())
    return total_score

def get_pair_score(filename, known_letter_pairs_freqs):
    """ count the occurrences of each pair of letters on our deciphered output text, and multiply that count with
        the known frequency of that pair, which is given in the "Letter_Freq2" file.
    """
    # a dict to count occurrences of each pair of letters (keys copied from known_letter_pairs_freqs)
    pair_counter = collections.Counter(dict.fromkeys(known_letter_pairs_freqs.keys(), 0))
    with open(filename, 'r') as f:
        deciphered_file = f.read().lower()
    # Run through all pairs in the file and count their occurrences
    for i in range(len(deciphered_file) - 1):
        pair = deciphered_file[i:i + 2]
        if pair in pair_counter:
            pair_counter[pair] += 1

    # Multiply the count of each pair by the known frequency of that pair
    pair_scores = {pair: count * known_letter_pairs_freqs[pair] for pair,count in pair_counter.items()}
    # Sum up the scores to get the total score
    total_score = sum(pair_scores.values())
    return total_score

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
def compare_freqs(perm_letter_freqs, known_letter_freqs):
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
    # TODO: this code will be removed
    # file_score = 0
    # important_words = {"i", "a"}
    # with open(perm_deciphered_file, "r") as deciphered_file:
    #     for line in deciphered_file:
    #         words = line.split()
    #         for word in words:
    #             if word.isalpha():
    #                 if word.lower() in common_words:
    #                     # If the word is in common_words, increment the score with COMMON_WORDS_SCORE
    #                     file_score += COMMON_WORDS_SCORE
    #                 elif word.lower in important_words:
    #                     # If the word is in important_words, increment the score with IMPORTANT_WORDS_SCORE
    #                     file_score += IMPORTANT_WORDS_SCORE
    # return file_score

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


# new combined func
def get_common_words_info(perm_deciphered_file, common_words):
    """
    This single function will calculate both the common words score and the intersect percentage.
     By using the set output_words to keep track of unique words in the file,
     it can calculate the intersection with common_words.
      This method also prevents having to open and read the file twice.
      The function now returns two values - perm_words_score and intersect_percentage.

     Analyzes the content of a given file and calculates two metrics:
    1. perm_words_score: a score based on the frequency of common and important words in the file,
     normalized by total word count.
    2. intersect_percentage: the percentage of unique words in the file that intersect with a given set of common words.
    Args: perm_deciphered_file (str): The name of the file to analyze.
        common_words (set): A set of common words to check against.
    Returns: tuple: perm_words_score (float) and intersect_percentage (float)
    """
    # variables for calculating score
    perm_words_score = 0
    common_words_found = 0
    important_words_found = 0
    output_word_count = 0
    important_words = {"i", "a"}
    # variables for calculating intersection
    intersect_percentage = 0
    output_words = set()

    with open(perm_deciphered_file, "r") as deciphered_file:
        for line in deciphered_file:
            words = line.split()
            output_word_count += len(words)
            for word in words:
                if word.isalpha():
                    word_lower = word.lower()
                    output_words.add(word_lower)
                    if word_lower in common_words:
                        common_words_found += 1
                    elif word_lower in important_words:
                        important_words_found += 1

        # compute the final score
        if output_word_count != 0:
            perm_words_score = (common_words_found * COMMON_WEIGHT +
                                important_words_found * IMPORTANT_WEIGHT) / output_word_count

        # get the intersection percentage
        intersect_words_count = len(common_words.intersection(output_words))
        if output_words:
            # Calculate the percentage of intersecting words
            intersect_percentage = (intersect_words_count / len(output_words)) * 100
            intersect_percentage = round(intersect_percentage, 4)

    print("intersect_percentage: ", intersect_percentage)
    return perm_words_score, intersect_percentage



# if __name__ == '__main__':
#     global common_words, known_letter_freqs, known_letter_pairs_freqs
#
#     perm_letter_freqs = compute_perm_letter_freq('output.txt', known_letter_freqs)
#     # for letter, freq in sorted(perm_letter_freqs.items()):
#     #     print(f'{letter}: {freq:.4f}')
#
#     difference = compare_freqs(perm_letter_freqs, known_letter_freqs)
#     print(f'letters freq Total difference: {difference:.4f}')
#
#     pair_freqs = compute_letter_pairs_freq('output.txt', known_letter_pairs_freqs)
#     # for pair, freq in sorted(pair_freqs.items()):
#     #     print(f'{pair}: {freq:.4f}')
#
#     difference = compare_pairs_freqs(pair_freqs, known_letter_pairs_freqs)
#     print(f'pairs freq Total difference: {difference:.4f}')
#
