#-------------------------------------------------------------------------------
# Author: Justin Lewis Salmon <mccrustin@gmail.com>
#-------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

import argparse
import json
from sga import selection, crossover, mutation, fitness
from sga.population import Population
from sga.representation import Representation


def setup_args():
    """
    Return an object containing the command-line args, once they have been
    validated. Exit on error.
    """
    parser = argparse.ArgumentParser(description='Run a genetic algorithm.')

    #---------------------------------------------------------------------------
    # Add the necessary argument parameters
    #---------------------------------------------------------------------------
    parser.add_argument('-r', '--representation',
                        dest='representation',
                        action='store',
                        type=json.loads,
                        metavar="representation",
                        help='genome representation dictionary'
                             ' (default: {"type": "binary", "length": 50} )',
                        default={"type": "binary", "length": 50})
    parser.add_argument('-p', '--population-size',
                        dest='population_size',
                        action='store',
                        type=int,
                        metavar="population_size",
                        help='population size (default: 100)',
                        default=50)
    parser.add_argument('-g', '--generations',
                        dest='generations',
                        action='store',
                        type=int,
                        metavar="generations",
                        help='number of generations to simulate '
                             '(default: 1000)',
                        default=50)
    parser.add_argument('-s', '--selection-scheme',
                        dest='selection_scheme',
                        action='store',
                        metavar="selection_scheme",
                        help='selection scheme to use [roulette, tournament]'
                             ' (default: roulette)',
                        default='roulette')
    parser.add_argument('-C', '--crossover-scheme',
                        dest='crossover_scheme',
                        action='store',
                        metavar="crossover_scheme",
                        help='crossover scheme to use [single_point, uniform]'
                             ' (default: single_point)',
                        default='single_point')
    parser.add_argument('-M', '--mutation-scheme',
                        dest='mutation_scheme',
                        action='store',
                        metavar="mutation_scheme",
                        help='mutation scheme to use [bit_flip, swap]'
                             ' (default: bit_flip)',
                        default='bit_flip')
    parser.add_argument('-f', '--fitness-function',
                        dest='fitness_function',
                        action='store',
                        metavar="fitness_function",
                        help='fitness function to use [all_ones, matching_bits]'
                             ' (default: all_ones)',
                        default='all_ones')
    parser.add_argument('-n', '--natural-fitness',
                        dest='natural_fitness',
                        action='store_true',
                        help='use natural fitness values, i.e. higher fitness '
                             'value implies fitter individual (default)')
    parser.add_argument('-N', '--no-natural-fitness',
                        dest='natural_fitness',
                        action='store_false',
                        help='do not use natural fitness values, i.e. lower '
                             'fitness value implies fitter individual')
    parser.add_argument('-c', '--crossover-probability',
                        dest='crossover_probability',
                        action='store',
                        type=float,
                        metavar="crossover_probability",
                        help='probability of crossover occurring '
                             '(default: 0.6)',
                        default=0.5)
    parser.add_argument('-m', '--mutation-probability',
                        dest='mutation_probability',
                        action='store',
                        type=float,
                        metavar="mutation_probability",
                        help='probability of mutation occurring '
                             '(default: 0.01)',
                        default=0.01)
    parser.add_argument('-e', '--elite-count',
                        dest='elite_count',
                        action='store',
                        type=int,
                        metavar="elite_count",
                        help='number of fittest individuals to hold back at '
                             'each generation. Will be rounded up to an even '
                             'number (default: 6)',
                        default=6)
    parser.add_argument('-t', '--tournament-size',
                        dest='tournament_size',
                        action='store',
                        type=int,
                        metavar='tournament_size',
                        help='size of a tournament group, if tournament '
                             'selection is being used (default: 10)')

    parser.set_defaults(natural_fitness=True)

    #---------------------------------------------------------------------------
    # Get the user supplied arguments
    #---------------------------------------------------------------------------
    args = parser.parse_args()

    #-----------------------------------------------------------------------
    # Get the function pointers
    #-----------------------------------------------------------------------
    try:
        args.selection_scheme = getattr(selection, args.selection_scheme)
        args.crossover_scheme = getattr(crossover, args.crossover_scheme)
        args.mutation_scheme  = getattr(mutation,  args.mutation_scheme)
        args.fitness_function = getattr(fitness,   args.fitness_function)
    except AttributeError, e:
        raise e

    return args


def main():
    """
    Run a genetic algorithm.

    TODO:
        - Allow arbitrary representations (binary, real, enum, ...)
        - Add crossover and mutation funcs for these representations
        - Allow stateful/changing mutation and crossover probabilities
        - Allow constraint handling (repairing infeasible solutions, penalty
          functions, time-variable penalty functions)
        - Maybe include constraints in representations (JSON?)
    """
    args = setup_args()

    #---------------------------------------------------------------------------
    # Print a short summary
    #---------------------------------------------------------------------------
    print 'population size=%d, representation=%s, generations=%d, ' \
          'crossover probability=%f, mutation probability=%f, elite count=%d' \
          % (args.population_size, args.representation, args.generations,
             args.crossover_probability, args.mutation_probability,
             args.elite_count)
    print 'selection scheme=%s, crossover scheme=%s, mutation scheme=%s, ' \
          'fitness function=%s, natural_fitness=%s' \
          % (args.selection_scheme, args.crossover_scheme, args.mutation_scheme,
             args.fitness_function, args.natural_fitness)

    #---------------------------------------------------------------------------
    # Generate the initial population
    #---------------------------------------------------------------------------
    p = Population(representation=Representation(args.representation),
                   size=args.population_size,
                   fitness_func=args.fitness_function,
                   selection_func=args.selection_scheme,
                   crossover_func=args.crossover_scheme,
                   mutation_func=args.mutation_scheme,
                   natural_fitness=args.natural_fitness,
                   crossover_probability=args.crossover_probability,
                   mutation_probability=args.mutation_probability,
                   elite_count=args.elite_count,
                   tournament_size=args.tournament_size)
    p.gen_population()

    #---------------------------------------------------------------------------
    # Run the GA
    #---------------------------------------------------------------------------
    p.run(args.generations)

#-------------------------------------------------------------------------------
# Bootstrap
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
