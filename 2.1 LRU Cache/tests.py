import unittest
from cache import LRUCache


class LruTests(unittest.TestCase):
    def test_push_out(self):
        lru = LRUCache(3)
        initial_dict = {'Alice': 'Clark', 'Natasha': 'Rostova', 'Peter': 'Parker'}
        lru.update(initial_dict)
        lru.get('Alice')
        lru['Angela'] = 'Merkel'
        expected_keys = list(initial_dict.keys())
        expected_keys.pop(1)
        expected_keys.append('Angela')
        self.assertEqual(set(expected_keys), set(lru.keys()))

    def test_ordering(self):
        lru = LRUCache(3)
        lru.update({'Alice': 'Clark', 'Mark': 'Shagal'})
        lru['Keanu'] = 'Reeves'
        lru['Alice'] = 'Rostova'
        _ = lru['Mark']
        self.assertEqual(list(lru.keys()), ['Keanu', 'Alice', 'Mark'])

    def test_deletion(self):
        lru = LRUCache(3)
        lru.update({'Alice': 'Clark', 'Mark': 'Shagal'})
        lru['Keanu'] = 'Reeves'
        _ = lru['Alice']
        lru['Leonardo'] = 'Da Vinci'
        self.assertEqual(lru.get('Mark'), '')
        lru.delete('Keanu')
        self.assertEqual(lru.get('Keanu'), '')
        del lru['Leonardo']
        self.assertEqual(lru.get('Leonardo'), '')

    def test_never_existed(self):
        lru = LRUCache(10)
        self.assertEqual(lru.get('Anon'), '')

    def test_update(self):
        lru = LRUCache(2)
        lru.update({'1': 'one', '2': 'two', '3': 'three'})
        self.assertEqual(tuple(lru.keys()), ('2', '3'))


if __name__ == '__main__':
    unittest.main()
