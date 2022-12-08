"""
This is manual implementation of a hash table, inspired by page #88.

Python obviously already has a really good implementation of a hash table in
the form of a dict, but it's interesting to see what I can learn from this.
"""
import random
import unittest
from faker import Faker
from typing import Any

__all__ = ['HashTable']


class HashTable:
    """
    Key-value lookup data structure.

    Examples:

        ht = HashTable()
        ht.set("foo", 2)
        ht.get("foo")  # -> 2
        ht.get(0)  # -> None
        ht.get(0, "testing")  # => "testing"
        for key, val in ht:
            print(f'{key}: {val}')
    """
    def __init__(self):
        pass

    def __iter__(self):
        pass

    # TODO: we'll extend keys to be other things at a later time;
    # let's get integers working first
    def set(self, key: int, value: Any):
        pass

    def get(self, key: int, default_value: Any = None) -> Any:
        pass


class HashTableTests(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()

    def _random_value(self):
        methods = [method for method in dir(self.fake)
                   if not method.startswith('_')]
        func = getattr(self.fake, random.choice(methods))
        return func()

    def test_set_and_get__int_key(self):
        ht = HashTable()
        key = self.fake.random_int()
        value = self._random_value()
        ht.set(key, value)
        self.assertEqual(value, ht.get(key))


if __name__ == '__main__':
    unittest.main()
