from bisect import bisect_left
import random


def roulette(population):
    """Return a new population list after performing roulette wheel selection"""
    cumulative_fitnesses = list()
    cumulative_fitnesses.append(population[0].fitness())

    for i in xrange(1, len(population)):
        fitness = population[i].fitness()
        cumulative_fitnesses.append(cumulative_fitnesses[i - 1] + fitness)

    selection = list()
    for i in xrange(0, len(population)):

        random_fitness = int(random.random() * cumulative_fitnesses[-1])
        index = bisect_left(cumulative_fitnesses, random_fitness)

        if index < 0:
            index = abs(index + 1)

        selection.append(population[index])

    return selection


def tournament(population):
    """Return a new population list after performing tournament selection"""
    return population
