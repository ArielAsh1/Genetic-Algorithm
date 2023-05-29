# Genetic Algorithm for Decryption

This repository contains a Python program that implements a genetic algorithm for decrypting ciphers.
The genetic algorithm is designed to find the best permutation of characters that can decrypt a given cipher text.
It offers three types of algorithms: classic, Darwinian, and Lamarckian.

## Requirements

- Python 3.x

## Usage

1. Clone the repository to your local machine:
2. Navigate to the project directory
3. Run the program: GeneticAlgorithm.py 
4. Follow the prompts to choose the algorithm type (0 for classic, 1 for Darwinian, 2 for Lamarckian) and provide the required inputs.

## Algorithm Types

1. Classic Algorithm: This algorithm represents a basic implementation of a genetic algorithm for decryption. It generates random permutations of characters and evaluates their fitness based on the decrypted text. The fittest permutations are selected for reproduction, leading to the evolution of better solutions over generations. Crossover and mutation operations are applied to create new offspring.
2. Darwinian Algorithm: This algorithm builds upon the classic algorithm by introducing selection pressure to each permutation. If the pressure results in a better offspring, the algorithm will continue with the original permutation and its new evaluation score.
3. Lamarckian Algorithm: This algorithm extends the Darwinian algorithm by selecting both the new permutation and its evaluation score after applying selection pressure by mutating each permutation.

## Contributing

Contributions to this project are welcome! If you have any ideas, suggestions, or bug reports, please feel free to open an issue or submit a pull request.
