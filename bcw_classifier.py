import random
from classifier.BcwClassifier import BcwClassifier
from classifier.gene import Gene
from sga.population import Population


def main():
    data_file = 'classifier/data/bcw/breast-cancer-wisconsin.data.txt'
    data = list()

    #---------------------------------------------------------------------------
    # Load the data
    #---------------------------------------------------------------------------
    with open(data_file, 'r') as f:
        for line in f:
            data_line = list()

            # Split the line but throw away first number (ID number)
            line = line.split(',')[1:]

            # Store class label
            # data_line['class'] = line[-1]

            # Store data
            if '?' not in line:
                for item in line[:-1]:
                    data_line.append(normalise(float(item)))

                data_line.append(int(line[-1].rstrip()))
                data.append(data_line)

    num_genes = 40
    gene_length = 18  # lower + upper bound for each 9 data points

    classifier = BcwClassifier(data, num_genes, gene_length)

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
    for i, individual in enumerate(p.population):

        new_genes = list()
        average_sigmas = list()
        individual.average_sigmas = list()

        for genes in classifier.batch_gen(individual.genes,
                                          classifier.gene_length):
            g = Gene(genes)#[normalise(float(gene)) for gene in genes])
            g.class_label = 2 if random.random() < 0.5 else 4
            g.mutation_step_sizes = [0.015 for _
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

    data = list()
    for chunk in classifier.batch_gen(p.average_sigmas, p.size):
        data.append(sum(chunk) / len(chunk))

    p.add_to_plot(data, 'average sigma')

    for gene in p.max_individual().genes:
        for pair in classifier.batch_gen(gene.alleles, 2):
            print pair

        print gene.class_label
        print

    p.show_plot()


def normalise(x):
    """"""
    return (x - 0) / (10 - 0)

#-------------------------------------------------------------------------------
# Bootstrap
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
