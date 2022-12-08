"""
This is manual implementation of a hash table, inspired by page #88.

Python obviously already has a really good implementation of a hash table in
the form of a dict, but it's interesting to see what I can learn from this.
"""

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
    # TODO: let's get some type notation in here

    def __init__(self):
        pass

    def __iter__(self):
        pass

    def set(self, key, value):
        pass

    def get(self, key, default_value=None):
        pass
