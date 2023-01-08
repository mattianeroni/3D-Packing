
def resetCase(case):
    """ Reset the characteristics of a case """
    currentItem = case.__copy__()
    currentItem.busyCorners = [False, False, False]
    currentItem.canHold = currentItem.strength
    return currentItem
    

def rotate (case):
    """ Method used to rotate a case of 90° on the horizontal plan """
    case.rotated = not case.rotated
    case.sizex, case.sizey = case.sizey, case.sizex


class Case:
    
    """ One of the cases to place into the pallet """

    def __init__ (self, orderline, code, sizex, sizey, sizez, weight, strength):
        """
        :param orderline: The orderline the case belongs to
        :param code: The code of the case (the type of product it contains)
        :param sizex, sizey, sizez: The dimensions of the case
        :param weight: The weight of the case
        :param strength: The strenght of the case (i.e., the number of cases it can hold above)
        """
        self.orderline = orderline
        self.code = code
        self.x = 0
        self.y = 0
        self.z = 0
        self.rotated = False
        self.sizex = sizex
        self.sizey = sizey
        self.sizez = sizez
        self.volume = sizex * sizey * sizez
        self.weight = weight
        self.strength = strength
        self.canHold = strength
        self.busyCorners = [False, False, False]  # Used to speed up the DubePacker

    def __repr__(self):
        return f"Case(position={self.position}, size=({self.sizex}, {self.sizey}, {self.sizez})," \
                 f" weight={self.weight}, strength={self.strength}, rotated={self.rotated}, busyCorners={self.busyCorners})"

    def __copy__ (self):
        obj = Case.__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        obj.busyCorners = list(self.busyCorners)
        return obj

    @property
    def position (self):
        return self.x, self.y, self.z

    def setPosition(self, pos):
        self.x, self.y, self.z = pos

    @property
    def top (self):
        return self.z + self.sizez

    @property
    def bottom (self):
        return self.z

    @property
    def left (self):
        return self.x

    @property
    def right (self):
        return self.x + self.sizex

    @property
    def front (self):
        return self.y

    @property
    def back (self):
        return self.y + self.sizey
