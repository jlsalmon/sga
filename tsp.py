from sga.crossover import noop
from sga.mutation import swap
from sga.population import Population
from sga.representation import Representation
from sga.selection import tournament

#-------------------------------------------------------------------------------
# Map for the TSP problem with 15 cities
#-------------------------------------------------------------------------------
tsp_lau15_map = list()
with open("tsplib/lau15_dist.txt") as f:
    tsp_lau15_map = [[int(num) for num in line.split()] for line in f]

#-------------------------------------------------------------------------------
# Map for the TSP problem with 30 cities
#-------------------------------------------------------------------------------
tsp_ha30_map = list()
with open("tsplib/ha30_dist.txt") as f:
    tsp_ha30_map = [[int(num) for num in line.split()] for line in f]

#-------------------------------------------------------------------------------
# Map for the TSP problem with 29 cities
#-------------------------------------------------------------------------------
tsp_bays29_map = list()
tsp_bays29_names = list()
with open("tsplib/bays29.tsp") as f:

    tsp_bays29_map = [[int(num) for num in line.split()]
                      for line in f if not line.startswith('#')]


class TSP(object):
    """
    Class to help working with tsplib files from
    http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/
    """
    def __init__(self, tsp_file):

        with open(tsp_file) as f:
            self.tsp_map = [[int(num) for num in line.split()]
                            for line in f if not line.startswith('#')]
            self.city_names = [i for i in xrange(len(self.tsp_map))]

    def calc_tour(self, genome):
        """
        Generic TSP route calculator
        """
        if len(genome) != len(set(genome)):
            print genome
            raise ValueError('Tour invalid. Fix the crossover/mutation func')

        v = list()

        for i, gene in enumerate(genome):
            j = i + 1 if i != (len(genome) - 1) else 0
            v.append(self.tsp_map[genome[i]][genome[j]])

        return sum(v)


def main():
    """
    tsplib: bays29

    gen=500 cfunc=noop mfunc=swap sfunc=tournament
    ----------------------------------------------------------------------------
    size=50 cprob=0.5 mprob=0.5 ecnt=6 tsize=5 max=2333
    size=50 cprob=0.5 mprob=0.5 ecnt=6 tsize=10 max=2330
    size=50 cprob=0.5 mprob=0.5 ecnt=6 tsize=15 max=2455

    size=100 cprob=0.5 mprob=0.5 ecnt=6 tsize=5 max=2106
    size=100 cprob=0.5 mprob=0.5 ecnt=6 tsize=10 max=2319
    size=100 cprob=0.5 mprob=0.5 ecnt=6 tsize=15 max=2165

    size=100 cprob=0.5 mprob=0.7 ecnt=6 tsize=5 max=2352
    size=100 cprob=0.5 mprob=0.3 ecnt=6 tsize=5 max=
    """

    tsp = TSP('tsplib/bays29.tsp')

    #---------------------------------------------------------------------------
    # Generate the initial population
    #---------------------------------------------------------------------------
    representation = { "length": 5,
                       "type": "enum",
                       "values": tsp.city_names,
                       "duplicates": False }

    generations = 500

    p = Population(representation=Representation(representation),
                   size=100,
                   fitness_func=tsp.calc_tour,
                   selection_func=tournament,
                   crossover_func=noop,
                   mutation_func=swap,
                   natural_fitness=False,
                   crossover_probability=0.5,
                   mutation_probability=0.3,
                   elite_count=6)
    p.gen_population()

    #---------------------------------------------------------------------------
    # Run the GA
    #---------------------------------------------------------------------------
    p.run(generations)

#-------------------------------------------------------------------------------
# Bootstrap
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
