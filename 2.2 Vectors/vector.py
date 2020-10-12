class Vector(list):
    def __init__(self, initial_data):
        super().__init__(initial_data)

    def __add__(self, other):
        if not isinstance(other, (list, Vector)):
            raise ValueError
        diff = len(other) - len(self)
        return Vector(map(lambda x, y: x + y,
                          (self if diff > 0 else other) + [0] * abs(diff),
                          other if diff > 0 else self))

    def __sub__(self, other):
        if not isinstance(other, (list, Vector)):
            raise ValueError
        diff = len(other) - len(self)
        return Vector(map(lambda x, y: x - y,
                          self + ([0] * abs(diff) if diff > 0 else []),
                          other + ([] if diff >= 0 else [0] * abs(diff))))

    def __eq__(self, other):
        if not isinstance(other, (list, Vector)):
            raise ValueError
        return sum(self) == sum(other)

    def __le__(self, other):
        if not isinstance(other, (list, Vector)):
            raise ValueError
        return sum(self) <= sum(other)

    def __lt__(self, other):
        if not isinstance(other, (list, Vector)):
            raise ValueError
        return sum(self) < sum(other)

    def __gt__(self, other):
        if not isinstance(other, (list, Vector)):
            raise ValueError
        return sum(self) > sum(other)

    def __ge__(self, other):
        if not isinstance(other, (list, Vector)):
            raise ValueError
        return sum(self) >= sum(other)

    def __ne__(self, other):
        if not isinstance(other, (list, Vector)):
            raise ValueError
        return sum(self) != sum(other)