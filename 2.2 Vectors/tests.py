import unittest
from vector import Vector


class VectorTests(unittest.TestCase):
    def test_add(self):
        a = Vector([1, 2, 3, 4, 5])
        b = [1, 2, 3]
        self.assertEqual(list(a + b), [2, 4, 6, 4, 5])
        self.assertEqual(b, [1, 2, 3])
        c = Vector([-1, -2])
        self.assertEqual(list(a + c), [0, 0, 3, 4, 5])
        self.assertEqual(list(c), [-1, -2])

    def test_sub(self):
        a = Vector([1, 2, 3, 4, 5])
        b = [1, 2, 3]
        self.assertEqual(list(a - b), [0, 0, 0, 4, 5])
        self.assertEqual(b, [1, 2, 3])
        c = Vector([-1, -2])
        self.assertEqual(list(a - c), [2, 4, 3, 4, 5])
        self.assertEqual(list(c), [-1, -2])

    def test_comparissons(self):
        a = Vector([4, 4])
        b = [2, 2, 3]
        c = Vector([2, 2, 4])
        d = Vector([3, 4, 2])
        self.assertEqual(a, c)
        self.assertEqual(a, [8])
        self.assertGreater(d, a)
        self.assertGreaterEqual(d, a)
        self.assertLess(b, a)
        self.assertLessEqual(b, a)
        self.assertGreaterEqual(c, a)
        self.assertLessEqual(a, c)
        self.assertNotEqual(b, c)
        self.assertNotEqual(d, a)


if __name__ == '__main__':
    unittest.main()
