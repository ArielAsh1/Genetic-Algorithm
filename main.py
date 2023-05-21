
import random
import string

import heuristics

ELITE_PERCENT = 0.2
MUTATION_PERCENT = 0.1
DROPTOUT_PERCENT = 0.2
POPULATION_SIZE = 500


# global variables
common_words = set()
known_letter_freqs = {}
known_letter_pairs_freqs = {}


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
    # TODO: before submit check where the given files are located on the testers computers
    global common_words, known_letter_freqs, known_letter_pairs_freqs
    # Load the word list, and the letter and digraph frequencies
    with open('dict.txt', 'r') as f:
        common_words = set(line.strip() for line in f)

    # Create a dictionary where the key is the lowercase letter and the value is the frequency as a float.
    with open('Letter_Freq.txt', 'r') as f:
        known_letter_freqs = {line.strip().split('\t')[1].lower(): float(line.strip().split('\t')[0]) for line in f}

    # a dictionary mapping lowercase letter pairs to their frequencies
    # the key is the letters pair and the value is the frequency as a float.
    with open('Letter2_Freq.txt', 'r') as f:
        for line in f:
            # only proccess lines that contain a tab character
            if "\t" in line:
                known_letter_pairs_freqs[line.strip().split('\t')[1].lower()] = float(line.strip().split('\t')[0])
                # last line in file should be for "ZZ"
                if line.strip().split('\t')[1].lower() == "zz":
                    break


def get_fitness(perm_deciphered_file):
    """ return this current perm fitness result.
        lower fitness score means bad, higher means good score.
    """
    global common_words, known_letter_freqs, known_letter_pairs_freqs
    perm_total_score = 0
    # decreasing the absolut diff of the letter frequencies from the score
    # the closer the current perm letter frequency to the known letter frequency, less score will be decreased
    perm_letter_freqs = heuristics.compute_perm_letter_freq(perm_deciphered_file, known_letter_freqs)
    letter_freq_diff = heuristics.compare_freqs(perm_letter_freqs, known_letter_freqs)
    perm_total_score -= letter_freq_diff

    # decreasing the absolut diff of the letter pairs frequencies from the score
    pair_freqs = heuristics.compute_letter_pairs_freq(perm_deciphered_file, known_letter_pairs_freqs)
    pairs_freq_diff = heuristics.compare_pairs_freqs(pair_freqs, known_letter_pairs_freqs)
    perm_total_score -= pairs_freq_diff

    # increasing the score in response to how many common words were detected
    words_score = heuristics.search_common_words(perm_deciphered_file, common_words)
    perm_total_score += words_score

    return perm_total_score


def fitness_tal(perm_deciphered_file):
    """ return this current perm fitness result.
        lower fitness score means bad, higher means good score.
    """
    global common_words, known_letter_freqs, known_letter_pairs_freqs

    # get the scores
    letter_score = heuristics.get_letter_score(perm_deciphered_file, known_letter_freqs)
    pairs_score = heuristics.get_pair_score(perm_deciphered_file, known_letter_pairs_freqs)
    return letter_score + pairs_score


def generate_permutations(starting_population):
    alphabet = list(string.ascii_lowercase)
    permutations = []
    for _ in range(starting_population):
        random.shuffle(alphabet)
        permutation = {letter: substitute for letter, substitute in zip(string.ascii_lowercase, alphabet)}
        permutations.append(permutation)

    # returns a list of perm dicts
    return permutations


def crossover(p1, p2):
    """ This function performs a crossover on two given parent permutations (p1 and p2).
        The crossover generates new permutations (children) by combining parts of the two existing parents.
    """
    # Select a random point for the crossover
    crossover_point = random.randint(0, len(p1))
    child1 = {}
    child2 = {}

    # copy the perm up to the crossover point, from the parents to the children
    for i in range(crossover_point):
        key1, value1 = list(p1.items())[i]
        key2, value2 = list(p2.items())[i]
        child1[key1] = value1
        child2[key2] = value2

    # copy the perm from to the crossover point until the end, from the parents to the children
    # parents XX , YY will create children XY , YX
    for i in range(crossover_point, len(p1)):
        key1, value1 = list(p1.items())[i]
        key2, value2 = list(p2.items())[i]
        child1[key2] = value2
        child2[key1] = value1

    # Ensure that each child is a valid permutation (no duplicate values)
    check_duplicates(child1)
    check_duplicates(child2)
    return child1, child2


def check_duplicates(dictionary):
    """
    the function identifies duplicate values in the permutation dictionary,
    and identifies the unused letters (the letters which don't appear in this permutation as values).
    then it replaces each duplicate with a unique, unused letter.
    """
    # the values set holds the values that have already been seen
    values = set()
    duplicates = set()
    for value in dictionary.values():
        if value in values:
            duplicates.add(value)
        values.add(value)

    if duplicates:
        unused_letters = list(set(string.ascii_lowercase) - set(dictionary.values()))
        for key, value in dictionary.items():
            if len(unused_letters) == 0:
                break
            if value in duplicates:
                dictionary[key] = get_unique_value(values, unused_letters)


def get_unique_value(values, unused_letters):
    while True:
        unique_value = random.choice(unused_letters)
        if unique_value not in values:
            values.add(unique_value)  # Add the generated unique value to the set
            unused_letters.remove(unique_value)
            return unique_value


def perform_mutation(permutation):
    keys = list(permutation.keys())
    # TODO: necessary?
    if len(keys) < 2:
        return
    key1, key2 = random.sample(keys, 2)
    value1 = permutation[key1]
    value2 = permutation[key2]
    permutation[key1] = value2
    permutation[key2] = value1


def run_round(permutations):
    """ Defines a single generation in the genetic algorithm.
        Extracts the top percent of the permutations with the best fitness score to be used in the next round.
        The remaining permutations create children permutations by crossover, which will also be used in the next round.
        Together they make the new permutations list for the following round.
    """
    fitness_scores = []
    crossover_children = []
    for perm in permutations:
        find_and_replace(perm, "enc.txt", "output.txt")
        # TODO: decide on fitness function
        # fitness option 1:
        # curr_perm_score = get_fitness("output.txt")
        # fitness option 2:
        curr_perm_score = fitness_tal("output.txt")
        fitness_scores.append(curr_perm_score)

    # create a new indices DESC sorted list of the fitness scores, while fitness_scores maintains its original order.
    sorted_indices = sorted(set(range(len(fitness_scores))), key=lambda x: fitness_scores[x], reverse=True)
    # Calculate the number of the top scores that will be used in the next round
    num_top_scores = int(len(fitness_scores) * ELITE_PERCENT)
    num_dropout_scores = int(len(fitness_scores) * DROPTOUT_PERCENT)
    # Select these top ELITE_PERCENT of fitness scores and their corresponding permutations
    top_scores_indices = sorted_indices[:num_top_scores]
    remaining_indices = sorted_indices[:-num_dropout_scores]
    top_permutations = [permutations[index] for index in top_scores_indices]

    # extract the non-top permutations
    top_scores_set = set(remaining_indices)
    remaining_permutations = [permutations[i] for i in range(len(permutations)) if i in top_scores_set]
    # implement crossover on the non-top remaining_permutations
    for _ in range((POPULATION_SIZE - num_top_scores) // 2):
        # crossover between 2 non-top perms:
        # parent1, parent2 = random.sample(remaining_permutations, 2)
        # crossover between non-top and top perms:
        parent1 = random.sample(remaining_permutations, 1)
        parent2 = random.sample(top_permutations, 1)
        child1, child2 = crossover(parent1[0], parent2[0])
        crossover_children.append(child1)
        crossover_children.append(child2)

    # selecting a subset of the new crossover children for another mutation
    for _ in range(int(len(crossover_children) * MUTATION_PERCENT)):
        # Get a random permutation from the crossover children
        random_perm = random.choice(crossover_children)
        perform_mutation(random_perm)

    # prints to keep track of the algorithm progress
    print("best fitness score: ", max(fitness_scores))
    print("it's index: ", fitness_scores.index(max(fitness_scores)))
    # TODO: at some point the permutations stop changing
    print("it's permutation: ", permutations[fitness_scores.index(max(fitness_scores))])
    best_perm = permutations[fitness_scores.index(max(fitness_scores))]
    # create the deciphered file with the best perm we found
    find_and_replace(best_perm, "enc.txt", "output.txt")

    # add the top permutations to the crossover children and return as the next round permutations
    next_round_perms = crossover_children + top_permutations
    return next_round_perms


def check_common_words_usage():
    global common_words
    with open('output.txt', 'r') as f:
        output_words = set(line.strip() for line in f)
    intersect_words = len(common_words) - len(common_words - output_words)
    return intersect_words


if __name__ == '__main__':
    read_files()
    permutations = generate_permutations(POPULATION_SIZE)
    # TODO: run loop that checks for convergence
    for i in range(100):
        print("Round: ", i + 1)
        permutations = run_round(permutations)
        print("Num of intersecting words: " + str(len(check_common_words_usage())))


