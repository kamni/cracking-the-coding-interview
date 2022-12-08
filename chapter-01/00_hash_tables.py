"""
This is manual implementation of a hash table, inspired by page #88.

Python obviously already has a really good implementation of a hash table in
the form of a dict, but it's interesting to see what I can learn from this.
"""
import random
import unittest
from faker import Faker
from typing import Any, Hashable

__all__ = ['HashTable']


class HashNode:
    """
    Linked list structure for the Hash Table.
    """
    def __init__(self, key: Hashable, value: Any):
        self.key = key
        self.value = value
        self.hash_code = hash(key)
        self.next_node = None

    def __eq__(self, other: Any):
        # We rely on the key here, rather than the hash,
        # because two completely different things might share the same hash.
        # Presumably if the keys are equal,
        # they would also share the same hash.
        return (
            isinstance(other, HashNode) and
            self.key == other.key
        )


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

    def set(self, key: Hashable, value: Any):
        pass

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        pass

    # TODO: function for removal


def _random_value(fake):
    methods = [method for method in dir(fake)
               if not method.startswith('_')]
    func = getattr(fake, random.choice(methods))
    return func()


class HashNodeTests(unittest.TestCase):
    class AlwaysEqualHash:
        def __init__(self, value):
            self.value = value

        def __eq__(self, other):
            return self.value is other.value

        def __hash__(self):
            return 1

    def setUp(self):
        self.fake = Faker()

    def test_init(self):
        key = self.fake.word()
        value = _random_value(self.fake)
        node = HashNode(key, value)

        self.assertEqual(key, node.key)
        self.assertEqual(value, node.value)
        self.assertEqual(hash(key), node.hash_code)

    def test_eq__false(self):
        node1 = HashNode(self.AlwaysEqualHash(3), "foo")
        node2 = HashNode(self.AlwaysEqualHash(4), "bar")
        self.assertNotEqual(node1, node2)

    def test_eq__true(self):
        node1 = HashNode(self.AlwaysEqualHash(3), "foo")
        node2 = HashNode(self.AlwaysEqualHash(3), "bar")
        self.assertEqual(node1, node2)


class HashTableTests(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()

    def test_set_and_get__int_key(self):
        ht = HashTable()
        key = self.fake.random_int()
        value = _random_value(self.fake)
        ht.set(key, value)
        self.assertEqual(value, ht.get(key))


if __name__ == '__main__':
    unittest.main()
