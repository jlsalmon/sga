sga
===

Simple genetic algorithm implementation with user-defined genome representation and fitness/crossover/mutation schemes

Usage
-----

```
$ python sga.py --help
usage: sga.py [-h] [-r representation] [-p population_size] [-g generations]
              [-s selection_scheme] [-C crossover_scheme] [-M mutation_scheme]
              [-f fitness_function] [-c crossover_probability]
              [-m mutation_probability]

Run a genetic algorithm.

optional arguments:
  -h, --help            show this help message and exit
  -r representation, --representation representation
                        genome representation dictionary (default: {"type":
                        "binary", "length": 16} )
  -p population_size, --population-size population_size
                        population size (default: 100)
  -g generations, --generations generations
                        number of generations to simulate (default: 1000)
  -s selection_scheme, --selection-scheme selection_scheme
                        selection scheme to use [roulette, tournament]
                        (default: roulette)
  -C crossover_scheme, --crossover-scheme crossover_scheme
                        crossover scheme to use [single_point, uniform]
                        (default: single_point)
  -M mutation_scheme, --mutation-scheme mutation_scheme
                        mutation scheme to use [bit_flip, swap] (default:
                        bit_flip)
  -f fitness_function, --fitness-function fitness_function
                        fitness function to use [all_ones, matching_bits]
                        (default: all_ones)
  -c crossover_probability, --crossover-probability crossover_probability
                        probability of crossover occurring (default: 0.6)
  -m mutation_probability, --mutation-probability mutation_probability
                        probability of mutation occurring (default: 0.01)
```

Representation format
---------------------


