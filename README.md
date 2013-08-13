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

The representation format is a Python dictionary, passed on the command line,
which specifies the genome length, type, acceptable values, etc.

**Options**
***********

* `"length"`     : the length of the genome
* `"type"`       : the type of the genome ["int", "float", "binary", "enum"]
* `"min"`        : minimum value for a single allele (only valid for int and float
                 types, ignored for others)
* `"max"`        : maximum value for a single allele (only valid for int and float
                 types, ignored for others)
* `"values"`     : list of possible allele values (only valid for enum types)
* `"duplicates"` : whether duplicate alleles are allowed in a single genome

**Examples**
************

```
    # Binary
    {
     "length" : 16,
     "type"   : "binary"
    }

    # Integer
    {
     "length" : 10,
     "type"   : "int",
     "min"    : 0,
     "max"    : 100
    }

    # Real values
    {
     "length" : 10,
     "type"   : "float",
     "min"    : 0.0,
     "max"    : 1.0
    }

    # Enum
    {
     "length" : 4,
     "type"   : "enum"
     "values" : ["red", "blue", "green", "yellow"]
    }
```

Customising the algorithm
-------------------------

To allow greater flexibility, it is possible to define additional custom
functions for crossover, mutation and selection operations in addition to the
supplied built-in schemes.

**Selection**
*************

Roulette-wheel and tournament selection are supplied. To add a new selection
scheme, put your function in [selection.py](sga/selection.py). See that file
for reference implementations. The selection function takes a single parameter 
which will be the current population object (see [population.py](sga/population.py).
Your function should return a list containing the newly selected population
of genome objects (see [genome.py](sga/genome.py)).

**Crossover**
*************

Single-point and uniform crossover schemes are supplied. Add your custom crossover
function to [crossover.py](sga/crossover.py). The function will take 2 parameters,
both being individual genomes of your supplied representational format, and should
return two newly crossed-over children.

The library code determines whether your crossover function is called, so you do
not need to check for it in your code.

**Mutation**
************

Bit-flipping and swapping mutation schemes are supplied. Add your custom mutation
function to [mutation.py](sga/mutation.py). The function will take a single genome
of your supplied representational format, and it should return a newly mutated
genome of the same format.

The library code determines whether your mutation function is called, so you do
not need to check for it in your code.

Contact
-------

Problems? Submit an issue or email me. I happily accept pull requests!
