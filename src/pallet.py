import collections
import functools
import operator



def pallets_generator (size, max_weight):
    """ This is a generator of pallets with standard dimensions and weight
    capacity """
    while True:
        yield Pallet(size, max_weight)



class HashableDict (dict):
    """
    Implementation of a hashable dictionary. This implementation is needed to make
    pallets hashable and caching the packing function.
    """
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class Pallet:
    
    """ An instance of this class represents a pallet """

    def __init__ (self, size, max_weight):
        """
        :param size: The maximum pallet size (x, y, z)
        :param max_weight: The pallet weight capacity

        :attr layersMap: HashableDict {OrderLine : int} that keeps track of the layer
                        that each orderline occupies into the pallet.
                        This is very important to understand in which order the storage
                        locations can be visited.
        :attr orderlines: The set of orderlines stored into this pallet.
        """
        self.__i = 0             # Counter used to iterate the pallet cases
        self.size = size
        self.maxWeight = max_weight
        self.maxVolume = functools.reduce(operator.mul, size, 1)
        self.cases = collections.deque()
        self.layersMap = HashableDict()
        self.orderlines = set()
        self.weight = 0
        self.volume = 0

    def __hash__ (self):
        """ Method implemented to make the pallet hashable for caching """
        return hash(self.layersMap)

    @property 
    def max_can_hold (self):
        """ The maximum number of additional cases the pallet can hold """
        return max(i.canHold for case in self.cases)

    @property 
    def min_can_hold (self):
        """ The minimum number of additional cases the pallet can hold """
        return min(i.canHold for case in self.cases)

    def __iter__(self):
        self.__i = 0
        return self 

    def __next__(self):
        if self.__i < len(self.cases):
            self.__i += 1
            return self.cases[self.__i - 1]
        raise StopIteration