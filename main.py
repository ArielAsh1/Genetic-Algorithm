import random
import string
import sys
import copy
import statistics
import matplotlib.pyplot as plt
import numpy as np
import heuristics

INPUT_ENC = "enc.txt"
OUTPUT_FILE = "plain.txt"
ELITE_PERCENT = 0.2
MUTATION_PERCENT = 0.3
DROPOUT_PERCENT = 0.4
POPULATION_SIZE = 300
STUCK_THRESHOLD = 15
ROUNDS = 10


LETTER_WEIGHT = 1
PAIR_WEIGHT = 10
WORDS_WEIGHT = 5

# test1
TRUE_CODE = {'a': 'y', 'b': 'x', 'c': 'i', 'd': 'n', 'e': 't', 'f': 'o', 'g': 'z', 'h': 'j', 'i': 'c', 'j': 'e',
            'k': 'b', 'l': 'l', 'm': 'd', 'n': 'u', 'o': 'k', 'p': 'm', 'q': 's', 'r': 'v', 's': 'p', 't': 'q',
            'u': 'r', 'v': 'h', 'w': 'w', 'x': 'g', 'y': 'a', 'z': 'f'}
#test2
# TRUE_CODE = {
#     'a': 'q',
#     'b': 'w',
#     'c': 'e',
#     'd': 'r',
#     'e': 't',
#     'f': 'y',
#     'g': 'u',
#     'h': 'i',
#     'i': 'o',
#     'j': 'p',
#     'k': 'a',
#     'l': 's',
#     'm': 'd',
#     'n': 'f',
#     'o': 'g',
#     'p': 'h',
#     'q': 'k',
#     'r': 'j',
#     's': 'l',
#     't': 'z',
#     'u': 'x',
#     'v': 'c',
#     'w': 'v',
#     'x': 'b',
#     'y': 'n',
#     'z': 'm'
# }
# test3
# TRUE_CODE = {
#     'a': 'q',
#     'b': 'w',
#     'c': 'e',
#     'd': 'r',
#     'e': 't',
#     'f': 'y',
#     'g': 'u',
#     'h': 'i',
#     'i': 'o',
#     'j': 'p',
#     'k': 'a',
#     'l': 's',
#     'm': 'd',
#     'n': 'f',
#     'o': 'g',
#     'p': 'h',
#     'q': 'j',
#     'r': 'k',
#     's': 'l',
#     't': 'z',
#     'u': 'x',
#     'v': 'c',
#     'w': 'v',
#     'x': 'b',
#     'y': 'n',
#     'z': 'm'}

# global variables
common_words = set()
known_letter_freqs = {}
known_letter_pairs_freqs = {}
stats_list = []     # will hold tuples with (best, avg, worst) fintess scores of each round,
prev_best_fitness = -1000
round_first_seen_best_fitness = -1000
total_fitness_calls = 0


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


# TODO: update documentation and comments
def get_fitness(perm_deciphered_file):
    """ return this current perm fitness result.
        lower fitness score means bad, higher means good score.
    """
    global common_words, known_letter_freqs, known_letter_pairs_freqs, total_fitness_calls
    total_fitness_calls += 1

    # decreasing the absolut diff of the letter frequencies from the score
    # the closer the current perm letter frequency to the known letter frequency, less score will be decreased
    perm_letter_freqs = heuristics.compute_perm_letter_freq(perm_deciphered_file, known_letter_freqs)
    letter_freq_diff = heuristics.compare_letter_freqs(perm_letter_freqs, known_letter_freqs)

    # decreasing the absolut diff of the letter pairs frequencies from the score
    pair_freqs = heuristics.compute_letter_pairs_freq(perm_deciphered_file, known_letter_pairs_freqs)
    pairs_freq_diff = heuristics.compare_pairs_freqs(pair_freqs, known_letter_pairs_freqs)

    # increasing the score in response to how many common words were detected
    words_score = heuristics.get_common_words_score(perm_deciphered_file, common_words)

    # apply weights to score with respect to how significant each finding
    return -(letter_freq_diff * LETTER_WEIGHT) - (pairs_freq_diff * PAIR_WEIGHT) + (words_score * WORDS_WEIGHT)


def fitness_tal(perm_deciphered_file):
    """ return this current perm fitness result.
        lower fitness score means bad, higher means good score.
    """
    global common_words, known_letter_freqs, known_letter_pairs_freqs
    # TODO: problematic in the case where two letters have similar freq, how will it choose between them..? think if indeed a problem

    # get the scores
    letter_score = heuristics.get_letter_score(perm_deciphered_file, known_letter_freqs)
    pairs_score = heuristics.get_pair_score(perm_deciphered_file, known_letter_pairs_freqs)
    words_score = heuristics.get_common_words_score(perm_deciphered_file, common_words)
    # return letter_score + pairs_score + words_score

    return letter_score * LETTER_WEIGHT + pairs_score * PAIR_WEIGHT + words_score * WORDS_WEIGHT


def generate_permutations():
    alphabet = list(string.ascii_lowercase)
    permutations = []
    for _ in range(POPULATION_SIZE):
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


def check_duplicates(perm):
    """
    this function ensures the uniqueness of the permutation values.
    it identifies duplicate values in the permutation dictionary,
    and identifies the unused letters (the letters which don't appear in this permutation as values).
    then it replaces each duplicate with a unique, unused letter.
    """
    # the values set holds the values that have already been seen in this perm
    values = set()
    duplicates = set()
    # check if each value was seen before (a duplicate)
    for value in perm.values():
        if value in values:
            # if was seen before add it to duplicates
            duplicates.add(value)
        values.add(value)

    # if there are duplicates, create a list of unused letters
    if duplicates:
        unused_letters = list(set(string.ascii_lowercase) - set(perm.values()))
        for key, value in perm.items():
            if len(unused_letters) == 0:
                break
            if value in duplicates:
                # replace duplicate value with a unique value
                perm[key] = get_unique_value(values, unused_letters)


def get_unique_value(values, unused_letters):
    """
    The function is used to fetch a unique value (an unused letter) from the list of unused letters.
    the while loop continues until it finds a letter that is not already in the values set.
    """
    while True:
        unique_value = random.choice(unused_letters)
        if unique_value not in values:
            # Add the generated unique value to the set, and remove it from possible unused_letters
            values.add(unique_value)
            unused_letters.remove(unique_value)
            return unique_value


def perform_mutation(permutation):
    """ the function performs mutation on the permutation dict.
    """
    # TODO: mutate more than 2 values?
    keys = list(permutation.keys())
    # to avoid errors in case the permutation has less than two elements
    if len(keys) < 2:
        return
    key1, key2 = random.sample(keys, 2)
    value1 = permutation[key1]
    value2 = permutation[key2]
    # the mutation step, where two letters in the permutation are exchanged (swapping values)
    permutation[key1] = value2
    permutation[key2] = value1

def write_solution(best_perm):
    print(f"Total number of calls for fitness function is: {total_fitness_calls}")
    with open('perm.txt', 'w') as file:
        for key, value in best_perm.items():
            file.write(f'{key} {value}\n')


def before_exit():
    # todo: should plot from here
    exit()


def run_round(permutations, curr_round):
    """ Defines a single generation in the genetic algorithm.
        Extracts the top percent of the permutations with the best fitness score to be used in the next round.
        The remaining permutations create children permutations by crossover, which will also be used in the next round.
        Together they make the new permutations list for the following round.
    """
    global prev_best_fitness, round_first_seen_best_fitness, stats_list
    fitness_scores = []
    crossover_children = []
    for perm in permutations:
        find_and_replace(perm, INPUT_ENC, OUTPUT_FILE)
        # TODO: decide on fitness function
        # fitness option 1:
        curr_perm_score = round(get_fitness(OUTPUT_FILE), 5)
        # fitness option 2:
        # curr_perm_score = round(fitness_tal("output.txt"), 5)
        fitness_scores.append(curr_perm_score)

    # create a new indices DESC sorted list of the fitness scores, while fitness_scores maintains its original order.
    sorted_indices = sorted(set(range(len(fitness_scores))), key=lambda x: fitness_scores[x], reverse=True)
    # Calculate the number of the top scores that will be used in the next round
    num_top_scores = int(len(fitness_scores) * ELITE_PERCENT)
    num_dropout_scores = int(len(fitness_scores) * DROPOUT_PERCENT)
    # Select these top ELITE_PERCENT of fitness scores and their corresponding permutations
    top_scores_indices = sorted_indices[:num_top_scores]
    top_scores_set = set(top_scores_indices)
    top_permutations = [permutations[index] for index in top_scores_set]

    # extract the non-top permutations, excluding the dropout.
    remaining_indices = sorted_indices[:-num_dropout_scores]
    remaining_indices_set = set(remaining_indices) - top_scores_set
    remaining_permutations = [permutations[i] for i in range(len(permutations)) if i in remaining_indices_set]

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
        # TODO: mutate others as well/instead?
        random_perm = random.choice(crossover_children)
        perform_mutation(random_perm)

    ### prints to keep track of the algorithm progress
    curr_best_fitness = max(fitness_scores)
    curr_worst_fitness = min(fitness_scores)
    curr_avg_fitness = statistics.mean(fitness_scores)
    stats_list.append((curr_best_fitness, curr_avg_fitness, curr_worst_fitness))
    print("####### CURRENT ROUND BEST FITNESS SCORE: ", curr_best_fitness)
    # print("it's index: ", fitness_scores.index(curr_best_fitness))
    best_perm = permutations[fitness_scores.index(curr_best_fitness)]
    # print("it's permutation: ", best_perm)
    print("Equal percent: " + str(compare_dictionaries(best_perm, TRUE_CODE)))
    # create the deciphered file with the best perm we found so far (THIS PART SHOULD STAY AFTER TESTS)
    find_and_replace(best_perm, INPUT_ENC, OUTPUT_FILE)

    # add the top permutations to the crossover children and return as the next round permutations
    next_round_perms = crossover_children + top_permutations

    # convergence checks:
    if is_max_round(curr_round):
        print("Reached max rounds")
        write_solution(best_perm)
        before_exit()
        # sys.exit()
    elif intersection_percent_with_common_words(OUTPUT_FILE) == 100:
        print("CONVERGED, all deciphered output words are in common words")
        write_solution(best_perm)
        before_exit()
        # sys.exit()
    # check if fitness score is stuck
    elif is_stuck(curr_round, curr_best_fitness) < STUCK_THRESHOLD:
        # if not stuck
        if curr_best_fitness > prev_best_fitness:
            # update fitness global variables if improved #### TODO: should be if worsen as well???
            prev_best_fitness = curr_best_fitness
            round_first_seen_best_fitness = curr_round
        return next_round_perms
    else:
        # stuck, early convergence
        print("Stuck - fitness hasn't changed for:", STUCK_THRESHOLD, " rounds")
        write_solution(best_perm)
        before_exit()
        # sys.exit()


def check_local_optimum(permutation, old_fitness, N, typeFlag):
    """
    Function is responsible to run local optimum for Part B of the exercise.
    It performs a number (N) of mutations for input permutation, and than, according to the type of the run,
    returns the new/old permutation and its current fitness score.
    :param permutation: a permutation, which is a cnadidate for solution.
    :param old_fitness: the current fitness score of permutation.
    :param N: the number of mutations to perform on each permutation.
    :param typeFlag: 0 for darwin, 1 for lamarckian
    :return: if darwian - the old permutations and its new fitness score.
             if lamarckian - the new permutation and its new fitness score.
    """
    find_and_replace(permutation, INPUT_ENC, OUTPUT_FILE)
    old_fitness_score = round(get_fitness(OUTPUT_FILE), 5)

    new_permutation = copy.deepcopy(permutation)
    for i in range(N):
        perform_mutation(new_permutation)
    find_and_replace(new_permutation, INPUT_ENC, OUTPUT_FILE)
    new_fitness_score = round(get_fitness(OUTPUT_FILE), 5)
    if new_fitness_score > old_fitness_score:
        if typeFlag == 0:
            # darwian
            return permutation, new_fitness_score
        elif typeFlag == 1:
            # lamarckian
            return new_permutation, new_fitness_score
    else:
        return permutation, old_fitness_score


def run_round_darwin(permutations, curr_round, N, fitness_scores, typeFlag):
    global prev_best_fitness, round_first_seen_best_fitness
    crossover_children = []
    if curr_round == 0:
        # first round - should calculate fitness scores
        for perm in permutations:
            find_and_replace(perm, INPUT_ENC, OUTPUT_FILE)
            curr_perm_score = round(get_fitness(OUTPUT_FILE), 5)
            fitness_scores.append(curr_perm_score)

    # create a new indices DESC sorted list of the fitness scores, while fitness_scores maintains its original order.
    sorted_indices = sorted(set(range(len(fitness_scores))), key=lambda x: fitness_scores[x], reverse=True)
    # Calculate the number of the top scores that will be used in the next round
    num_top_scores = int(len(fitness_scores) * ELITE_PERCENT)
    num_dropout_scores = int(len(fitness_scores) * DROPTOUT_PERCENT)
    # Select these top ELITE_PERCENT of fitness scores and their corresponding permutations
    top_scores_indices = sorted_indices[:num_top_scores]
    top_scores_set = set(top_scores_indices)
    top_permutations = [permutations[index] for index in top_scores_set]

    # extract the non-top permutations, excluding the dropout.
    remaining_indices = sorted_indices[:-num_dropout_scores]
    remaining_indices_set = set(remaining_indices) - top_scores_set
    remaining_permutations = [permutations[i] for i in range(len(permutations)) if i in remaining_indices_set]

    # implement crossover on the non-top remaining_permutations
    for _ in range((POPULATION_SIZE - num_top_scores) // 2):
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

    joined_perms = top_permutations + crossover_children
    next_round_perms = []
    next_round_fitness = []
    for i in range(len(joined_perms)):
        perm = joined_perms[i]
        find_and_replace(perm, INPUT_ENC, OUTPUT_FILE)
        curr_fitness = round(get_fitness(OUTPUT_FILE), 5)
        # curr_fitness = fitness_scores[i]
        new_perm, new_fitness = check_local_optimum(perm, curr_fitness, N, typeFlag)
        next_round_perms.append(new_perm)
        next_round_fitness.append(new_fitness)


    ### prints to keep track of the algorithm progress
    curr_best_fitness = max(next_round_fitness)
    print("####### CURRENT ROUND BEST FITNESS SCORE: ", curr_best_fitness)
    # print("it's index: ", fitness_scores.index(curr_best_fitness))
    best_perm = next_round_perms[next_round_fitness.index(curr_best_fitness)]
    # print("it's permutation: ", best_perm)
    print("Equal percent: " + str(compare_dictionaries(best_perm, TRUE_CODE)))
    # create the deciphered file with the best perm we found so far (THIS PART SHOULD STAY AFTER TESTS)
    find_and_replace(best_perm, INPUT_ENC, OUTPUT_FILE)
    # add the top permutations to the crossover children and return as the next round permutations

    # convergence checks:
    if is_max_round(curr_round):
        print("Reached max rounds")
        write_solution(best_perm)
        sys.exit()
    elif intersection_percent_with_common_words(OUTPUT_FILE) == 100:
        print("CONVERGED, all deciphered output words are in common words")
        write_solution(best_perm)
        sys.exit()
    # check if fitness score is stuck
    elif is_stuck(curr_round, curr_best_fitness) < STUCK_THRESHOLD:
        # if not stuck
        if curr_best_fitness > prev_best_fitness:
            # update fitness global variables if improved #### TODO: should be if worsen as well???
            prev_best_fitness = curr_best_fitness
            round_first_seen_best_fitness = curr_round
        return next_round_perms, next_round_fitness
    else:
        # stuck, early convergence
        print("Stuck - fitness hasn't changed for:", STUCK_THRESHOLD, " rounds")
        write_solution(best_perm)
        sys.exit()


def main_PartB():
    read_files()
    permutations = generate_permutations()
    fitness_scores = []
    N = 5
    # 0 - darwian, 1 - lamarckian
    typeFlag = 0
    for i in range(ROUNDS):
        print("Round: ", i + 1)
        permutations, fitness_scores = run_round_darwin(permutations, i, N, fitness_scores, typeFlag)

def is_stuck(curr_round, curr_best_fitness):
    """ checks for early convergence-
        checks if the fitness score is stuck and stays the same for STUCK_THRESHOLD rounds.
    """
    global prev_best_fitness, round_first_seen_best_fitness

    if curr_best_fitness == prev_best_fitness:
        # if fitness stays the same, compute the rounds diff from the first time we saw this fitness
        rounds_diff = curr_round - round_first_seen_best_fitness
        return rounds_diff
    else:
        # fitness improved/worsen, return 0 which will simply mean 'not stuck'
        return 0


# check if reached max rounds
def is_max_round(curr_round):
    if curr_round == ROUNDS - 1:
        return True
    else:
        return False


def intersection_percent_with_common_words(perm_deciphered_file):
    """ calculates and returns the percentage of common words that appear in this permutation output file.
    """
    global common_words
    intersect_percentage = 0
    output_words = set()

    with open(perm_deciphered_file, "r") as deciphered_file:
        for line in deciphered_file:
            words = line.split()
            for word in words:
                if word.isalpha():
                    word_lower = word.lower()
                    output_words.add(word_lower)

        # get the intersection percentage
        intersect_words_count = len(common_words.intersection(output_words))
        if output_words:
            # Calculate the percentage of intersecting words
            intersect_percentage = (intersect_words_count / len(output_words)) * 100
            intersect_percentage = round(intersect_percentage, 4)

    print("intersection percentage: ", intersect_percentage)
    return intersect_percentage


# helper function FOR TESTS ONLY, true_perm will not be accessible in the real world
def compare_dictionaries(curr_perm, true_perm):
    matches = 0
    for key in curr_perm:
        if curr_perm[key] == true_perm[key]:
            matches += 1
    total_pairs = len(curr_perm)
    match_percentage = (matches / total_pairs) * 100
    return match_percentage, f"{matches}/{total_pairs}"


if __name__ == '__main__':
    # main_PartB()
    read_files()
    permutations = generate_permutations()
    for i in range(ROUNDS):
        print("Round: ", i + 1)
        permutations = run_round(permutations, i)
