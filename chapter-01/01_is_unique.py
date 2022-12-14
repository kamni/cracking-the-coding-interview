"""
1.1
Is Unique: Implement an algorithm to determine if a string has all unique
characters. What if you cannot use additional data structures?

Hints:

#44: Try a hash table.

#117: Could a bit vector be useful?

#132: Can you solve it in O(N log N) time? What might a solution like that
look like?
"""
import random
import string
import unittest

def is_unique(string: str):
    return False


class IsUniqueTests(unittest.TestCase):
    def test_empty_string(self):
        self.assertTrue(is_unique(''))

    def test_single_character(self):
        test_char = random.choice(string.printable)
        self.assertTrue(is_unique(test_char))

    def test_unique(self):
        self.assertTrue(is_unique(string.printable))

    def test_not_unique(self):
        test_char = random.choice(string.printable)
        test_char_array = [random.choice(string.printable)
                           for i in range(random.randint(10, 20))]
        for i in range(random.randint(2, 4)):
            test_char_array.insert(
                random.randrange(0, len(test_char_array)),
                test_char,
            )
        test_str = ''.join(test_char_array)
        self.assertFalse(is_unique(test_str))


if __name__ == '__main__':
    unittest.main()
