
import random
import string

import heuristics

ELITE_PERCENT = 0.1
MUTATION_PERCENT = 0.05
POPULATION_SIZE = 100
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


def generate_permutations(starting_population):
    alphabet = list(string.ascii_lowercase)
    permutations = []
    for _ in range(starting_population):
        random.shuffle(alphabet)
        permutation = {letter: substitute for letter, substitute in zip(string.ascii_lowercase, alphabet)}
        permutations.append(permutation)

    # returns list of perm dicts
    return permutations


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
        unused_letters = list(set(string.ascii_lowercase) - set(dictionary.values()))
        for key, value in dictionary.items():
            if value in duplicates:
                dictionary[key] = get_unique_value(values, unused_letters)


def get_unique_value(values, unused_letters):
    while True:
        unique_value = random.choice(unused_letters)
        if unique_value not in values:
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
    fitness_scores = []
    children = []
    for perm in permutations:
        find_and_replace(perm, "enc.txt", "output.txt")
        curr_perm_score = get_fitness("output.txt")
        fitness_scores.append(curr_perm_score)
        # print(perm)
        # print(curr_perm_score)
    # TODO: dear Orr, insert your index sorting magic here
    # Sort fitness scores while maintaining their indices
    sorted_indices = sorted(set(range(len(fitness_scores))), key=lambda x: fitness_scores[x], reverse=True)
    # Define the top X percent of fitness scores to consider
    top_percent = ELITE_PERCENT
    # Calculate the number of top scores to consider
    num_top_scores = int(len(fitness_scores) * top_percent)
    # Select the top X percent of fitness scores and their corresponding permutations
    top_scores_indices = sorted_indices[:num_top_scores]
    # # Append top permutations to children
    # for index in top_scores_indices:
    #     children.append(permutations[index])
    top_permutations = [permutations[index] for index in top_scores_indices]
    # todo: implement crossover on the leftovers
    # crossover the remainder of population
    top_scores_set = set(top_scores_indices)
    remaining_permutations = [permutations[i] for i in range(len(permutations)) if i not in top_scores_set]
    for i in range((POPULATION_SIZE - num_top_scores) // 2):
        parent1, parent2 = random.sample(remaining_permutations, 2)
        child1, child2 = crossover(parent1, parent2)
        children.append(child1)
        children.append(child2)

    # todo: mutate some of the left overs
    # mutate MUTATION_PERCENT from the remainder of permutations
    for j in range(int(POPULATION_SIZE * MUTATION_PERCENT)):
        # Get a random permutation from remaining_permutations
        random_permutation = random.choice(children)    # should be remaining_permutations?
        perform_mutation(random_permutation)

    print(max(fitness_scores))
    children.extend(top_permutations)
    return children


if __name__ == '__main__':
    read_files()
    permutations = generate_permutations(POPULATION_SIZE)
    # TODO: run loop that checks for convergence
    for i in range(100):
        permutations = run_round(permutations)


