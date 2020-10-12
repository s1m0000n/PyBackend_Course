from collections import OrderedDict


class LRUCache(OrderedDict):
    """LRU(least recently used) caching implementation based on OrderedDict
    with higher level wrappers"""
    def __init__(self, size=10) -> None:
        super().__init__()
        self.size = size

    def __getitem__(self, key: str) -> str:
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key: str, value: str) -> None:
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > self.size:
            del self[next(iter(self))]

    def __delitem__(self, key: str) -> None:
        super().__delitem__(key)

    def set(self, key: str, value: str) -> None:
        """Higher level wrapper of __setitem__"""
        self[key] = value

    def get(self, key: str) -> str:
        """Higher level wrapper of __getitem__
        In case of absence returns '' instead of raising KeyError"""
        return self[key] if key in self else ''

    def delete(self, key: str) -> None:
        """Higher level wrapper of __delitem__"""
        self.__delitem__(key)
