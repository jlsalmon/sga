import random
import sys
import numpy
from classifier.BinaryClassifier import BinaryClassifier
from classifier.RealValueClassifier import RealValueClassifier, chunker
from classifier.VariableLengthBinaryClassifier import \
    VariableLengthBinaryClassifier
from classifier.gene import Gene
from sga.population import Population
from sga.selection import tournament


def main():
    """
    Run the classification GA on the data file given on the the command line
    """
    if len(sys.argv) != 2:
        sys.exit('usage: classifier.py datafile')

    data_file = sys.argv[1]

    with open(data_file, 'r') as f:
        # Read the first (informational) line
        info_line = f.readline().split()

        # Set length of variables + class
        gene_length = int(info_line[3]) + 1
        # Derive the length of an individual
        genome_length = (int(info_line[0]) * gene_length)

        # Binary data (data1.txt)
        if genome_length == 192:
            data = [list(line.rstrip().replace(' ', '')) for line in f]
            classifier = BinaryClassifier(data, gene_length,
                                          genome_length)

        # Binary data (data2.txt)
        elif genome_length == 448:
            data = [list(line.rstrip().replace(' ', '')) for line in f]
            classifier = VariableLengthBinaryClassifier(data, gene_length,
                                                        genome_length)

        # Real-valued data
        elif genome_length == 14000:
            data = [map(float, line.rstrip().split()) for line in f]
            # 2 floats (upper, lower) per "bit", plus class
            gene_length = (gene_length * 2) - 2
            genome_length = (int(info_line[0]) * gene_length)
            classifier = RealValueClassifier(data, gene_length,
                                             genome_length)

        else:
            raise IOError('unknown data file format')

        print '[i] loaded data file:', data_file

    #---------------------------------------------------------------------------
    # Generate the initial population
    #---------------------------------------------------------------------------
    generations = classifier.generations

    p = Population(representation=classifier.representation,
                   size=classifier.population_size,
                   fitness_func=classifier.fitness_func,
                   selection_func=classifier.selection_func,
                   crossover_func=classifier.crossover_func,
                   mutation_func=classifier.mutation_func,
                   natural_fitness=True,
                   crossover_probability=classifier.crossover_prob,
                   mutation_probability=classifier.mutation_prob,
                   elite_count=classifier.elite_count,
                   tournament_size=classifier.tournament_size)
    p.gen_population()

    #---------------------------------------------------------------------------
    # Fiddle the population (ugly hack alert)
    #---------------------------------------------------------------------------
    step = classifier.gene_length

    if isinstance(classifier, VariableLengthBinaryClassifier):
        for individual in p:
            # Fix a 0 or 1 in the class position
            for i in xrange(step - 1, len(individual.genes), step):
                if individual.genes[i] == '#':
                    individual.genes[i] = '1' if random.random() < 0.5 else '0'

            classifier.genome_lengths.append(len(individual.genes))

    if isinstance(classifier, RealValueClassifier):
        for i, individual in enumerate(p.population):

            new_genes = list()
            average_sigmas = list()
            individual.average_sigmas = list()

            for genes in classifier.batch_gen(individual.genes,
                                              classifier.gene_length):
                g = Gene(genes)
                g.class_label = 1 if random.random() < 0.5 else 0
                g.mutation_step_sizes = [0.05 for _
                                         in xrange(classifier.gene_length)]
                new_genes.append(g)

                # Update info for plotter
                average_sigmas.append(sum(g.mutation_step_sizes)
                                      / len(g.mutation_step_sizes))

            individual.genes = new_genes

            individual.average_sigmas.append(sum(average_sigmas)
                                             / len(average_sigmas))
            # Add strategy parameters
            individual.strategy_params = {'mutation_step_size':
                                          0.05}

    print '[i] fiddled population'

    # if hasattr(classifier, 'genome_lengths'):
    #     p.add_to_plot([len(i) for i in p], 'avg genome length')

    #---------------------------------------------------------------------------
    # Run the GA
    #---------------------------------------------------------------------------
    p.run(generations)

    #---------------------------------------------------------------------------
    # Validate the population
    #---------------------------------------------------------------------------
    print
    avg = 0
    for individual in p:
        avg += classifier.fitness_func(individual.genes, validate=True)
    print 'min individual: %d/%dt, %d/%dv (len=%d, num genes=%d) %s' % \
          (classifier.fitness_func(p.min_individual().genes),
           len(classifier.training_set),
           classifier.fitness_func(p.min_individual().genes, validate=True),
           len(classifier.validation_set),
           len(p.min_individual()),
           len(p.min_individual()) / classifier.gene_length,
           p.min_individual())
    print 'mean validation fitness:', avg / len(p)
    print 'max individual: %d/%dt, %d/%dv (len=%d, num genes=%d) %s' % \
          (classifier.fitness_func(p.max_individual().genes),
           len(classifier.training_set),
           classifier.fitness_func(p.max_individual().genes, validate=True),
           len(classifier.validation_set),
           len(p.max_individual()),
           len(p.max_individual()) / classifier.gene_length,
           p.max_individual())

    # TODO: plot amount of generalisation

    if isinstance(classifier, VariableLengthBinaryClassifier):
        data = list()
        for chunk in classifier.chunker(classifier.genome_lengths, p.size):
            data.append(sum(chunk) / len(chunk))

        p.add_to_plot(data, 'avg genome length')

        for gene in classifier.chunker(p.max_individual().genes,
                                         classifier.gene_length):
            print gene[:-1], gene[-1]

    elif isinstance(classifier, RealValueClassifier):
        data = list()
        for chunk in chunker(p.average_sigmas, p.size):
            data.append(sum(chunk) / len(chunk))

        p.add_to_plot(data, 'average sigma')

        for gene in p.max_individual().genes:
            for pair in chunker(gene.alleles, 2):
                print pair

            print gene.class_label
            print

    p.show_plot()

#-------------------------------------------------------------------------------
# Bootstrap
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
