import unittest
from read_animals import breed


class TestJsonParser(unittest.TestCase):

    def test_breed(self):
        parent1 = {'head': 'snake', 'body': 'sheep-bunny', 'arms': 2, 'legs': 12, 'tail': 14}
        parent2 = {'head': 'snake', 'body': 'parrot-bream', 'arms': 6, 'legs': 6, 'tail': 12}

        child = {'head': 'snake', 'body': 'parrot-bream', 'arms': 2, 'legs': 6, 'tail': 8}

        self.assertEqual(breed(parent1, parent2), child)
        self.assertRaises(TypeError, breed, 'parent1', 'parent2')
        self.assertRaises(TypeError, breed, 1, 1)


if __name__ == '__main__':
    unittest.main()


