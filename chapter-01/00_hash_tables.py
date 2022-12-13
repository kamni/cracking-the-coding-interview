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
        self.hash_code = self.hash_code(key)
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
        if self == next_node:
            self.value = next_node.value
            return 0
        elif self.next_node:
            return self.next_node.add(next_node)
        else:
            self.next_node = next_node
            return 1

    @classmethod
    def hash_code(cls, key: Hashable) -> int:
        return hash(key)



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
        idx = self._get_table_index(node.hash_code)
        if self._table[idx] is None:
            self._table[idx] = node
            return 1
        else:
            return self._table[idx].add(node)

    def _get_table_index(self, hash_code: int):
        return abs(hash_code) % self._size

    def _is_too_full(self):
        return (
            (1.0 * self._number_of_nodes / self._size)
            >= self._MAX_FULLNESS_RATIO
        )

    def _rebuild_table(self):
        new_ht = HashTable(self._size * 2)
        for node in self:
            new_ht._add(node)
        self._table = new_ht._table
        self._size = new_ht._size

    def set(self, key: Hashable, value: Any):
        """
        Sets the `key` in the table with the assigned `value`.
        """
        node = HashNode(key, value)
        self._number_of_nodes += self._add(node)

        # Check to see if we might need to allocate more space to the table,
        # to keep performance close to O(1)
        if self._is_too_full():
            self._rebuild_table()

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        search_node = HashNode(key, None)
        table_idx = self._get_table_index(search_node.hash_code)
        start_node = self._table[table_idx]

        if start_node:
            for node in start_node:
                if search_node == node:
                    return node.value

        return default_value

    def delete(self, key: Hashable) -> Any:
        search_node = HashNode(key, None)
        table_idx = self._get_table_index(search_node.hash_code)
        previous_node = self._table[table_idx]

        if search_node == previous_node:
            self._table[table_idx] = previous_node.next_node
            self._number_of_nodes -= 1
            return previous_node.value
        elif previous_node:
            next_node = previous_node.next_node
            while next_node:
                if search_node == next_node:
                    previous_node.next_node = next_node.next_node
                    self._number_of_nodes -= 1
                    return next_node.value

        return None


def _random_value(fake):
    methods = [method for method in dir(fake)
               if not (method.startswith('_')
                       or method in [
                           'enum',
                           'format',
                           'get_formatter',
                           'provider'
                           'unique',
                       ])]
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
        node1 = HashNode(1, 1)
        node2 = HashNode(2, 2)
        node3 = HashNode(3, 3)
        node1.add(node2)
        node2.add(node3)
        self.assertEqual(
            [node1, node2, node3],
            [node for node in node1],
        )

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

        self.assertEqual(1, node1.add(node2))
        self.assertEqual(1, node1.add(node3))
        self.assertEqual(node1.next_node, node2)
        self.assertEqual(node2.next_node, node3)

    def test_add__duplicates(self):
        node1 = HashNode("foo", "bar")
        node2 = HashNode("foo", "baz")

        self.assertEqual(0, node1.add(node2))
        self.assertEqual("baz", node1.value)

        node3 = HashNode("bar", "baz")
        node4 = HashNode("bar", "buz")

        self.assertEqual(1, node1.add(node3))
        self.assertEqual(0, node1.add(node4))
        self.assertEqual("buz", node3.value)

    def test_hash_code(self):
        key1 = self.fake.random_int()
        self.assertEqual(hash(key1), HashNode.hash_code(key1))

        key2 = self.fake.word()
        self.assertEqual(hash(key2), HashNode.hash_code(key2))


class HashTableTests(unittest.TestCase):
    class FixedHash:
        def __init__(self, hash_code):
            self.hash_code = hash_code

        def __eq__(self, other: 'FixedHash'):
            return self.hash_code == other.hash_code

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
        node4 = HashNode(self.FixedHash(0), "test4")

        self.assertEqual(1, ht._add(node1))
        self.assertEqual(1, ht._add(node2))
        self.assertEqual(1, ht._add(node3))
        self.assertEqual(0, ht._add(node4))
        self.assertEqual(node1, ht._table[0])
        self.assertEqual(node2, ht._table[1])
        self.assertEqual(node3, ht._table[0].next_node)

    def test_get_table_index__positive_hash(self):
        ht = HashTable()
        key = self.FixedHash(13)
        self.assertEqual(
            13 % HashTable._INITIAL_SIZE,
            ht._get_table_index(hash(key)),
        )

    def test_get_table_index__negative_hash(self):
        ht = HashTable()
        key = self.FixedHash(-22)
        self.assertEqual(
            22 % HashTable._INITIAL_SIZE,
            ht._get_table_index(hash(key)),
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
        ht = HashTable(3)
        node1 = HashNode(0, 0)
        node2 = HashNode(2, 2)
        node3 = HashNode(3, 3)
        node4 = HashNode(5, 5)
        for node in [node1, node2, node3, node4]:
            ht._add(node)

        self.assertEqual(node1, ht._table[0])
        self.assertEqual(node2, ht._table[2])
        self.assertEqual(node3, ht._table[0].next_node)
        self.assertEqual(node4, ht._table[2].next_node)

        ht._rebuild_table()

        self.assertEqual(6, ht._size)
        self.assertEqual(node1, ht._table[0])
        self.assertEqual(node2, ht._table[2])
        self.assertEqual(node3, ht._table[3])
        self.assertEqual(node4, ht._table[5])

    def test_get__non_existing_node(self):
        ht = HashTable()
        self.assertIsNone(ht.get("foo"))

    def test_get__non_existing_node_with_default_value(self):
        ht = HashTable()
        self.assertEqual("bar", ht.get("foo", "bar"))

    def test_set_and_get(self):
        ht = HashTable()
        key1 = self.fake.random_int()
        value1 = _random_value(self.fake)
        ht.set(key1, value1)

        self.assertEqual(value1, ht.get(key1))
        self.assertEqual(1, ht._number_of_nodes)

        key2 = self.fake.word()
        value2 = _random_value(self.fake)
        ht.set(key2, value2)

        self.assertEqual(value2, ht.get(key2))
        self.assertEqual(2, ht._number_of_nodes)

    def test_set__existing_node(self):
        ht = HashTable()
        ht.set("foo", "bar")

        self.assertEqual("bar", ht.get("foo"))
        self.assertEqual(1, ht._number_of_nodes)

        ht.set("foo", "baz")

        self.assertEqual("baz", ht.get("foo"))
        self.assertEqual(1, ht._number_of_nodes)

    def test_set__redo_table_when_full(self):
        ht = HashTable(2)
        self.assertEqual(2, len(ht._table))
        self.assertEqual(2, ht._size)

        ht.set("foo", 1)
        ht.set("bar", 2)
        self.assertEqual(4, len(ht._table))
        self.assertEqual(4, ht._size)

    def test_delete__empty_table(self):
        ht = HashTable()
        self.assertIsNone(ht.delete("foo"))

    def test_delete__doesnt_exist(self):
        ht = HashTable(3)
        for fhash in [self.FixedHash(0), self.FixedHash(1), self.FixedHash(2)]:
            ht.set(fhash, "test")
        self.assertIsNone(ht.delete(self.FixedHash(3)))

    def test_delete__first_entry_no_next(self):
        ht = HashTable(10)
        test_fhash = self.FixedHash(1)
        ht.set(self.FixedHash(0), "test1")
        ht.set(test_fhash, "test2")
        ht.set(self.FixedHash(10), "test3")

        self.assertEqual(3, ht._number_of_nodes)
        self.assertEqual(test_fhash, ht._table[1].key)

        self.assertEqual("test2", ht.delete(test_fhash))
        self.assertIsNone(ht.get(test_fhash))
        self.assertEqual(2, ht._number_of_nodes)
        self.assertIsNone(ht._table[1])

    def test_delete__first_entry_with_next(self):
        ht = HashTable(10)
        test_fhash = self.FixedHash(0)
        next_fhash = self.FixedHash(10)
        ht.set(test_fhash, "test1")
        ht.set(self.FixedHash(1), "test2")
        ht.set(next_fhash, "test3")

        self.assertEqual(3, ht._number_of_nodes)
        self.assertEqual(test_fhash, ht._table[0].key)

        self.assertEqual("test1", ht.delete(test_fhash))
        self.assertIsNone(ht.get(test_fhash))
        self.assertEqual(2, ht._number_of_nodes)
        self.assertEqual(next_fhash, ht._table[0].key)

    def test_delete__second_entry_no_next(self):
        ht = HashTable(10)
        test_fhash = self.FixedHash(10)
        ht.set(self.FixedHash(0), "test1")
        ht.set(self.FixedHash(1), "test2")
        ht.set(test_fhash, "test3")

        self.assertEqual(3, ht._number_of_nodes)
        self.assertEqual(test_fhash, ht._table[0].next_node.key)

        self.assertEqual("test3", ht.delete(test_fhash))
        self.assertIsNone(ht.get(test_fhash))
        self.assertEqual(2, ht._number_of_nodes)
        self.assertIsNone(ht._table[0].next_node)

    def test_delete__second_entry_with_next(self):
        ht = HashTable(10)
        test_fhash = self.FixedHash(10)
        next_fhash = self.FixedHash(20)
        ht.set(self.FixedHash(0), "test1")
        ht.set(test_fhash, "test2")
        ht.set(next_fhash, "test3")

        self.assertEqual(3, ht._number_of_nodes)
        self.assertEqual(test_fhash, ht._table[0].next_node.key)

        self.assertEqual("test2", ht.delete(test_fhash))
        self.assertIsNone(ht.get(test_fhash))
        self.assertEqual(2, ht._number_of_nodes)
        self.assertEqual(next_fhash, ht._table[0].next_node.key)


if __name__ == '__main__':
    unittest.main()
