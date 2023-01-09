import collections


def assignPallet(orderline, pallet):
    """
    Function that could be used to assign a pallet to
    a orderline.

    :param orderline: The orderline 
    :param pallet: The pallet
    """
    orderline.pallet = pallet
    return orderline



class OrderLine:
    
    """ An instance of this class represents a customer orderline """
    
    def __init__ (self, cases=None):
        """
        :param cases: The cases required.
        """
        self.__i = 0            # Counter used to iterate the pallet cases
        self.cases = cases or tuple()
        self.weight = 0
        self.volume = 0
        self.pallet = None

    @property 
    def code (self):
        """ The required product 
        NOTE: We suppose each orderline contains one and only one product.
        """
        if self.cases:
            return self.cases[0].code 


    @property 
    def strength (self):
        """ The strength of the orderline 
        NOTE: We suppose each orderline contains one and only one product.
         """
        if self.cases:
            return self.cases[0].strength 


    def __repr__(self):
        return f"OrderLine(code={self.code}, n={len(self.cases)})"


    def __hash__(self):
        """
        Method implemented to make the OrderLine hashable. This is needed for caching
        and for using the orderlines as keys in a dictionary.
        """
        return hash(str(self))


    def __lt__(self, other):
        """
        The hashable orderlines must also be sortable. This is needed
        for caching using orderlines as keys.
        """
        return self.code < other.code


    def __iter__(self):
        self.__i = 0
        return self 


    def __next__(self):
        if self.__i < len(self.cases):
            self.__i += 1
            return self.cases[self.__i - 1]
        raise StopIteration