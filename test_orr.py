import random
import string

common_words_set = set()
letter_freqs = {}
letters_pair_freq = {}

def find_and_replace(permutation, input_file, output_file):
    """
    function will read the input file, and will create an outout.txt file that replaces the char according to the
    input permutation dictionary.
    """
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
    global common_words_set, letter_freqs, letters_pair_freq
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


def generate_permutations(starting_population):
    alphabet = list(string.ascii_lowercase)
    permutations = []
    for _ in range(starting_population):
        random.shuffle(alphabet)
        permutation = {letter: substitute for letter, substitute in zip(string.ascii_lowercase, alphabet)}
        permutations.append(permutation)
    return permutations


def search_common_words(file):
    # TODO: should iterate over words in output file, and search for words that appear in common_words
    # TODO: test score for words match - not necessarily be 1.
    global common_words_set
    file_score = 0
    important_words = {"i", "a"}
    with open("output.txt", "r") as f:
        for line in file:
            words = line.split()
            for word in words:
                if word.isalpha():
                    if word.lower() in common_words_set:
                        file_score += 1
                    elif word.lower in important_words:
                        file_score += 5
    return file_score


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

