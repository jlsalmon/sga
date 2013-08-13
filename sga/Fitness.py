

def all_ones(genome):
    """Return the number of 1s in the given binary-encoded genome"""
    return len([i for i in genome if int(i) == 1])


def matching_bits(genome):
    """Return the number of consecutive pairs of matching bits"""
    # TODO
    return 10


def all_small(genome):
    """Return the number of floats less than 0.1"""
    return len([i for i in genome if i < 0.1])


def all_a(genome):
    """Return the number of "a"s in the given genome"""
    return len([i for i in genome if i == 'a'])
