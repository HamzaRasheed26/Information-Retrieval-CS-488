class Node:
    """Node class to store key-value pairs in a linked list for handling collisions."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class CustomDictionary:
    """Custom dictionary data structure with basic hash table implementation."""

    def __init__(self, size=500):
        self.size = size
        self.table = [None] * self.size

    def _hash(self, key):
        """Hashes the key to an index based on the size of the table."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Inserts a key-value pair into the dictionary."""
        index = self._hash(key)
        if not self.table[index]:
            self.table[index] = Node(key, value)
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value  # Update existing key
                    return
                if not current.next:
                    break
                current = current.next
            current.next = Node(key, value)  # Insert new node at the end

    def get(self, key):
        """Retrieves the value associated with the given key."""
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"Key '{key}' not found.")

    def items(self):
        """Yields key-value pairs stored in the dictionary."""
        for node in self.table:
            current = node
            while current:
                yield current.key, current.value
                current = current.next

    def delete(self, key):
        """Deletes a key-value pair from the dictionary."""
        index = self._hash(key)
        current = self.table[index]
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                return
            prev = current
            current = current.next
        raise KeyError(f"Key '{key}' not found.")

    def __repr__(self):
        """Returns a string representation of the dictionary."""
        items = []
        for i, node in enumerate(self.table):
            while node:
                items.append(f"{node.key}: {node.value}")
                node = node.next
        return "{" + ", ".join(items) + "}"
