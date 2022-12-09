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


class HashNodeIterator:
    """
    HashNodes are linked lists; this is an iterator for HashNodes.
    """

    def __init__(self, head_node: 'HashNode'):
        self.current_node = head_node

    def __iter__(self):
        return self

    def __next__(self):
        if not self.current_node:
            raise StopIteration

        node = self.current_node
        self.current_node = self.current_node.next_node
        return node


class HashNode:
    """
    Linked list structure for the Hash Table.
    """
    # Linked lists are used primarily in languages where we don't have
    # resizeable arrays, unlike python.
    # We could use a regular python list to handle the nodes,
    # but this is more fun because it involves more work/learning.
    def __init__(self, key: Hashable, value: Any):
        self.key = key
        self.value = value
        self.hash_code = hash(key)
        self.next_node = None

    def __iter__(self):
        return HashNodeIterator(self)

    def __eq__(self, other: Any):
        # We rely on the key here, rather than the hash,
        # because two completely different things might share the same hash.
        # Presumably if the keys are equal,
        # they would also share the same hash.
        return (
            isinstance(other, HashNode) and
            self.key == other.key
        )

    def add(self, next_node: 'HashNode'):
        if self.next_node:
            self.next_node.add(next_node)
        else:
            self.next_node = next_node


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
    _INITIAL_SIZE = 10
    _MAX_FULLNESS_RATIO = 0.7

    def __init__(self, initial_size: int = _INITIAL_SIZE):
        self._table = [None for i in range(initial_size)]
        self._size = initial_size
        self._number_of_nodes = 0

    def __iter__(self):
        for node in self._table:
            if not node:
                continue
            for subnode in node:
                yield subnode

    def _add(self, node: 'HashNode'):
        idx = self._get_table_index(node)
        if self._table[idx] is None:
            self._table[idx] = node
        else:
            self._table[idx].add(node)

    def _get_table_index(self, node: 'HashNode'):
        return abs(node.hash_code) % self._size

    def _is_too_full(self):
        return (
            (1.0 * self._number_of_nodes / self._size)
            >= self._MAX_FULLNESS_RATIO
        )

    def _rebuild_table(self):
        new_ht = HashTable(self.size * 2)
        for node in self:
            new_ht._add(node)
        self._table = new_ht._table

    def set(self, key: Hashable, value: Any):
        """
        Sets the `key` in the table with the assigned `value`.
        """
        node = HashNode(key, value)

        # We don't want to increment the number of nodes,
        # if this node already exists
        if not self.get(key):
            self._number_of_nodes += 1
        self._add(node)

        # Check to see if we might need to allocate more space to the table,
        # to keep performance close to O(1)
        if self._is_too_full():
            self._rebuild_table()

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        pass

    # TODO: function for removal
    # Don't forget to decrement self._number_of_nodes


def _random_value(fake):
    methods = [method for method in dir(fake)
               if not (method.startswith('_') or method == 'enum')]
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

    def test_iter(self):
        node1 = None

    def test_iter__no_other_nodes(self):
        node1 = HashNode(1, 1)
        self.assertEqual([node1], [node for node in node1])

    def test_eq__false(self):
        node1 = HashNode(self.AlwaysEqualHash(3), "foo")
        node2 = HashNode(self.AlwaysEqualHash(4), "bar")
        self.assertNotEqual(node1, node2)

    def test_eq__true(self):
        node1 = HashNode(self.AlwaysEqualHash(3), "foo")
        node2 = HashNode(self.AlwaysEqualHash(3), "bar")
        self.assertEqual(node1, node2)

    def test_add(self):
        node1 = HashNode("foo", "bar")
        node2 = HashNode("bar", "baz")
        node3 = HashNode("baz", "buz")
        node1.add(node2)
        node1.add(node3)
        self.assertEqual(node1.next_node, node2)
        self.assertEqual(node2.next_node, node3)


class HashTableTests(unittest.TestCase):
    class FixedHash:
        def __init__(self, hash_code):
            self.hash_code = hash_code

        def __hash__(self):
            return self.hash_code

    def setUp(self):
        self.fake = Faker()

    def test_init__default(self):
        ht = HashTable()
        self.assertEqual(HashTable._INITIAL_SIZE, len(ht._table))
        self.assertEqual(HashTable._INITIAL_SIZE, ht._size)

    def test_iter(self):
        ht = HashTable(3)
        nodes = [
            HashNode(self.FixedHash(0), "node1"),
            HashNode(self.FixedHash(1), "node2"),
            HashNode(self.FixedHash(2), "node3"),
            HashNode(self.FixedHash(3), "node4"),
            HashNode(self.FixedHash(4), "node5"),
            HashNode(self.FixedHash(6), "node6"),
        ]
        for node in nodes:
            ht._add(node)
        self.assertEqual(
            [nodes[0], nodes[3], nodes[5], nodes[1], nodes[4], nodes[2]],
            [node for node in ht],
        )

    def test_iter__no_items(self):
        ht = HashTable()
        self.assertEqual([], [node for node in ht])

    def test_init__set_size(self):
        ht = HashTable(2)
        self.assertEqual(2, len(ht._table))
        self.assertEqual(2, ht._size)

    def test_add(self):
        ht = HashTable(2)
        node1 = HashNode(self.FixedHash(0), "test1")
        node2 = HashNode(self.FixedHash(1), "test2")
        node3 = HashNode(self.FixedHash(2), "test3")
        ht._add(node1)
        ht._add(node2)
        ht._add(node3)

        self.assertEqual(node1, ht._table[0])
        self.assertEqual(node2, ht._table[1])
        self.assertEqual(node3, ht._table[0].next_node)

    def test_get_table_index__positive_hash(self):
        ht = HashTable()
        node = HashNode(self.FixedHash(13), "node")
        self.assertEqual(
            13 % HashTable._INITIAL_SIZE,
            ht._get_table_index(node),
        )

    def test_get_table_index__negative_hash(self):
        ht = HashTable()
        node = HashNode(self.FixedHash(-22), "node")
        self.assertEqual(
            22 % HashTable._INITIAL_SIZE,
            ht._get_table_index(node),
        )

    def test_is_too_full__true(self):
        ht = HashTable()
        ht._size = 10
        ht._number_of_nodes = 7
        self.assertTrue(ht._is_too_full())

    def test_is_too_full__false(self):
        ht = HashTable()
        ht._size = 10
        ht._number_of_nodes = 6
        self.assertFalse(ht._is_too_full())

    def test_rebuild_table(self):
        raise NotImplementedError

    def test_set_and_get__int_key(self):
        ht = HashTable()
        key = self.fake.random_int()
        value = _random_value(self.fake)
        ht.set(key, value)
        self.assertEqual(value, ht.get(key))

    def test_set__existing_node(self):
        raise NotImplementedError

    def test_set__redo_table_when_full(self):
        raise NotImplementedError

if __name__ == '__main__':
    unittest.main()
