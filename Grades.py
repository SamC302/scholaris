import enum


class Grade(enum.Enum):
    A = .895
    B = .795
    C = .695
    D = .595
    E = 0

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        elif other.__class__ is int:
            return self.value > other
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        elif other.__class__ is int:
            return self.value >= other
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        elif other.__class__ is int:
            return self.value < other
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        elif other.__class__ is int:
            return self.value <= other
        return NotImplemented
