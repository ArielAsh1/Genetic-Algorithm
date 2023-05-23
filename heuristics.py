import collections
import string

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
    """ The function iterates over words in the text of the created deciphered file,
        and searches for matches with the words in the given common_words given.
        it also tries to match some specified important words.
        It assigns scores based on the frequency of these words.
    """
    
    # TODO- turn this pseudo to actual working code, which will replace the current code:
    # ######## start of pseudo
    # score = 0
    # common_words_found = 0
    # important_words_found = 0
    # output_word_count = 200
    # while reading words from output file:
    #     word
    #     if word is common:
    #         common_words_found += 1
    #     elif word is important:
    #         important_words_found += 1
    # score = (common_words_found * COMMON_WEIGHT + important_words_found * IMPORTANT_WEIGHT) / output_word_count
    # return score
    # # (we want IMPORTANT_WEIGHT > COMMON_WEIGHT)
    # ######## end of pseudo
    
    #TODO: this code will be removed (but some of it is useful and can be copied for the new code above)
    file_score = 0
    important_words = {"i", "a"}
    with open("output.txt", "r") as f:
        for line in perm_deciphered_file:
            words = line.split()
            for word in words:
                if word.isalpha():
                    if word.lower() in common_words:
                        # If the word is in common_words, increment the score with COMMON_WORDS_SCORE
                        file_score += COMMON_WORDS_SCORE
                    elif word.lower in important_words:
                        # If the word is in important_words, increment the score with IMPORTANT_WORDS_SCORE
                        file_score += IMPORTANT_WORDS_SCORE
    return file_score


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
