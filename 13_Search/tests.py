import unittest
from main import text_distance


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(text_distance('abc', 'aabbcc'), 3)
        self.assertEqual(text_distance('abcc', 'aabbcd'), 3)
        self.assertEqual(text_distance('abc', ''), 3)


if __name__ == '__main__':
    unittest.main()