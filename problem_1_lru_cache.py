class DoublyLinkedListNode:
    def __init__(self, key, value) -> None:
        self.previous = None
        self.key = key
        self.value = value
        self.next = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head = None
        self.tail = None

    def add(self, node):
        if node is None:
            return
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.previous = node
            self.head = node

    def remove(self, node):
        if node is None:
            return
        if self.head == self.tail:
            self.head = None
            self.tail = None
        elif node.previous and node.next:
            node.previous.next = node.next
            node.next.previous = node.previous
        elif not node.previous:
            self.head = node.next
            self.head.previous = None
        else:
            self.tail = node.previous
            self.tail.next = None
        node = None

    def pop_tail(self) -> DoublyLinkedListNode:
        if self.tail is None:
            return
        popped_node = self.tail
        self.tail = self.tail.previous
        self.tail.next = None
        return popped_node

    def __repr__(self) -> str:
        list_repr = ""
        node = self.head
        while node:
            list_repr += f"{{{node.key}:{node.value}}} --> "
            node = node.next
        return list_repr[:-5]


class LRU_Cache:
    def __init__(self, capacity) -> None:
        self.cache = {}
        self.list = DoublyLinkedList()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            old_node = self.cache[key]
            value = old_node.value
            self.list.remove(old_node)
            node = DoublyLinkedListNode(key, value)
            self.list.add(node)
            return value
        else:
            return -1

    def set(self, key, value) -> None:
        node = DoublyLinkedListNode(key, value)
        if len(self.cache) < self.capacity:
            self.cache[key] = node
            self.list.add(node)
        else:
            node_to_remove = self.list.pop_tail()
            key_to_remove = node_to_remove.key
            self.cache.pop(key_to_remove)
            self.cache[key] = node
            self.list.add(node)

    def __repr__(self) -> str:
        cache_repr = ""
        for k, node in self.cache.items():
            cache_repr += f"{k}: Node[{node.value}], "
        return (
            f"Hash Table: {{{cache_repr[:-2]}}}"
            + "\n"
            + f"Doubly Linked List: {self.list}"
        )


def udacity_tests():
    lru_cache = LRU_Cache(5)
    results = []

    for k, v in [(1, 1), (2, 2), (3, 3), (4, 4)]:
        lru_cache.set(k, v)

    for k in [1, 2, 9]:
        results.append(lru_cache.get(k))

    for k, v in [(5, 5), (6, 6)]:
        lru_cache.set(k, v)

    for k in [3]:
        results.append(lru_cache.get(k))

    assert results == [1, 2, -1, -1]


def my_tests():
    # Test 1 - Test for strings and integers
    lru_cache = LRU_Cache(5)
    results = []

    for k, v in [("Hello", "World"), (2, 2), (3, "Value3"), ("Key4", 4)]:
        lru_cache.set(k, v)

    for k in [2, "Key4", "Hello", 3]:
        results.append(lru_cache.get(k))

    assert results == [2, 4, "World", "Value3"]

    # Test 2 - Test for non-existent None key and string key
    lru_cache = LRU_Cache(5)
    results = []

    for k in [None, "A key"]:
        results.append(lru_cache.get(k))

    assert results == [-1, -1]

    # Test 3 - Test for setting and getting None
    lru_cache = LRU_Cache(5)
    results = []

    for k, v in [(None, None), (1, 2)]:
        lru_cache.set(k, v)

    for k in [None]:
        results.append(lru_cache.get(k))

    none_results = results
    assert none_results == [None]

    # Test 4 - Test for setting and getting repeated None
    lru_cache = LRU_Cache(5)
    results = []

    for k, v in [
        (None, None),
        (None, "A value"),
        ("A key", None),
        ("Another key", "Another Value"),
    ]:
        lru_cache.set(k, v)

    for k in [None, "A key", None, "Another key"]:
        results.append(lru_cache.get(k))

    assert results == ["A value", None, "A value", "Another Value"]

    # Test 5 - Test for single node in list
    lru_cache = LRU_Cache(5)
    results = []

    for k, v in [(1, 2)]:
        lru_cache.set(k, v)

    for k in [1]:
        results.append(lru_cache.get(k))

    assert results == [2]

    # Test 6 - Test for empty values
    lru_cache = LRU_Cache(5)
    results = []

    for k, v in [("A key", ""), ("", "A value")]:
        lru_cache.set(k, v)

    for k in ["A key", ""]:
        results.append(lru_cache.get(k))

    assert results == ["", "A value"]

    # Test 7 - Test for empty key with empty value
    lru_cache = LRU_Cache(5)
    results = []

    for k, v in [("", "")]:
        lru_cache.set(k, v)

    for k in [""]:
        results.append(lru_cache.get(k))

    empty_results = results
    assert empty_results == [""]

    # Test 8 - Test for very large values
    lru_cache = LRU_Cache(5)
    results = []

    for k, v in [
        (10**42, 7),
        (99**99, "A very large value"),
        ("Key to a large value", 123456789**99),
    ]:
        lru_cache.set(k, v)

    for k in ["Key to a large value", 10**42, 99**99]:
        results.append(lru_cache.get(k))

    large_results = results
    assert large_results == [123456789**99, 7, "A very large value"]

    # Print null, empty and large test results to meet project requirements
    print(none_results == [None]) # Should print True
    print(empty_results == [""]) # Should print True
    print(large_results == [123456789**99, 7, "A very large value"]) # Should print True

udacity_tests()
my_tests()
