import random


def bit_flip(genome):
    """Return the given genome after flipping a random bit

    Note: only works for binary representations
    """
    fmt = '{0:0' + str(len(genome)) + 'b}'
    print genome
    return fmt.format(int(genome, 2) ^ 1
                      << random.randint(0, len(genome)))[:len(genome)]


def swap(genome):
    """Return the given genome after randomly swapping two alleles"""
    r1 = random.randint(0, len(genome) - 1)
    r2 = random.randint(0, len(genome) - 1)
    genome[r1], genome[r2] = genome[r2], genome[r1]
    return genome
