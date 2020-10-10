from collections import OrderedDict


class LRUCache(OrderedDict):
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
        self[key] = value

    def get(self, key: str) -> str:
        return self[key] if key in self else ''

    def delete(self, key: str) -> None:
        self.__delitem__(key)