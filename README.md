# Data Structures Project

## Problem 1: Least Recently Used (LRU) Cache

### Efficiency

The code runs in constant time, O(1).

- For a get operation:

  - A value (node) is calculated given a key parsed into a hash map (a python dictionary). This is O(1).
  - The value (node) is removed from a Doubly Linked LIst. This is O(1).
  - The value (node) is added as the head of the list, which again runs in O(1).

- For a put (set) operation, either:
  - A value is extracted by parsing a key to a hash map (dictionary) and a node added to the doubly linked list, both operations are O(1); or,
  - The tail node is removed from the doubly linked list and key removed from the hash map (essentially setting the bucket at the known index from the hash function to None). The new node is then added to the dictionary and list, all operations of which are O(1).

### Design choices

- A python dictionary was chosen over implementing a hash map from scratch. This was done both primarily for simplicity.
- If a hash map were to be implemented, the hash function would generate a bucket index using by summing a prime-number based product of the Unicode character encoding for a given str(key). The index would feed into a bucket array.
- Collisions could be handled through separate chaining.
- The time complexity on average for adding and removing items to this implemented hash map would be on average O(1), depending on the initial array size and load factor chosen.
- Python's SipHash hash function for dictionaries has good performance characteristics and rarely encounters collisions out of the box, causing the practical time order to be closer to O(1) than perhaps the hash function discussed prior.
