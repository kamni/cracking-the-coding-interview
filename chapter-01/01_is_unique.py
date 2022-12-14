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


def is_unique_quicksort(string: str):
    """
    Mimics the quicksort algorithm to find duplicates.
    """
    def _sort(string_list, list_start, list_end):
        pivot = string_list[list_end]
        idx = list_start - 1
        for jdx in range(list_start, list_end):
            swapped = string_list[jdx]
            if swapped == pivot:
                return (-1, False)
            elif swapped < pivot:
                idx += 1
                string_list[jdx] = string_list[idx]
                string_list[idx] = swapped

        idx += 1
        string_list[list_end] = string_list[idx]
        string_list[idx] = pivot
        return (idx, True)

    def _is_unique(string_list, list_start, list_end):
        if not list_start < list_end:
            return True

        idx, is_unique = _sort(string_list, list_start, list_end)
        if is_unique:
            return (
                _is_unique(string_list, list_start, idx - 1) and
                _is_unique(string_list, idx + 1, list_end)
            )
        return False

    # Strings are immutable in Python,
    # so we have to change this into an list.
    # Unfortunately, this makes the algorithm O(N)...
    # perhaps we should just use a dict?
    string_list = list(string)
    return _is_unique(list(string), 0, len(string_list) - 1)


class IsUniqueQuicksortTests(unittest.TestCase):
    def test_empty_string(self):
        self.assertTrue(is_unique_quicksort(''))

    def test_single_character(self):
        test_char = random.choice(string.printable)
        self.assertTrue(is_unique_quicksort(test_char), test_char)

    def test_unique(self):
        self.assertTrue(is_unique_quicksort(string.printable))

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
        self.assertFalse(
            is_unique_quicksort(test_str),
            f'test_char: {test_char}\ntest_str: {test_str}',
        )


if __name__ == '__main__':
    unittest.main()
