class Representation(object):
    """
    # Binary
    {
     "length" : 16,
     "type"   : "binary"
    }

    # Integer values
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
     "type"   : "enum:
     "values" : ["red", "blue", "green", "yellow"]
    }

    # TSP
    {
     "length"     : 10,
     "values"     : ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
     "duplicates" : False
    }
    """

    def __init__(self, representation):
        self.representation = representation

        self.length = representation['length']
        self.type = representation['type']

        if 'values' in representation:
            self.values = representation['values']
        else:
            self.values = None

        if 'min' in representation:
            self.min = representation['min']
        else:
            if self.type in ('int', 'float'):
                self.min = 0
            else:
                self.min = None

        if 'max' in representation:
            self.max = representation['max']
        else:
            if self.type == 'int':
                self.max = 100
            elif self.type == 'float':
                self.max = 1
            else:
                self.max = None

        if 'duplicates' in representation:
            self.duplicates = representation['duplicates']
        else:
            self.duplicates = True
