cdef class Gene(object):
    cdef public list alleles
    cdef public class_label
    cdef public list mutation_step_sizes

    def __init__(self, alleles):
        self.alleles = alleles

    def __repr__(self):
        return repr(self.alleles)

    def __len__(self):
        return len(self.alleles)

    def __iter__(self):
        return iter(self.alleles)
