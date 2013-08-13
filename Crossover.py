import random


def single_point(male, female):
    """Return two new children after performing single point crossover"""
    crossover_point = random.randint(0, len(male))

    # sexy time
    child1 = male[:crossover_point] + female[crossover_point:]
    child2 = male[crossover_point:] + female[:crossover_point]

    return child1, child2


def uniform(male, female):
    """Return two new children after performing uniform crossover"""
    return male, female
