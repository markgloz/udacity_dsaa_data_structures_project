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

## Problem 2: File recursion

### Efficiency

Time complexity is related to the number of subdirectories and files contained within the path given.
It is linear time complexity, O(n), where n represents the number of unique subpaths in the given path.
The base case of the solution is if the path being evaluated is a file, then it returns the path of that file.
The recursive case is if the path being evaluated is a directory.

### Design choices

Recursive function with a for loop chosen due to simplicity in implementation and readiblity.
Each path is only evaluated once, making the efficiency linear.

## Problem 3: Huffman Coding

### Efficiency

- Time complexity is O(n logn).
- n represents the number of characters in a string of data
- Calculating frequencies of characters, O(n)
- Time complexity of insertion into a min heap is O(logn) in the worst case, as it has to traverse up the height of tree, equal to log(n)
- Current implementation of building the min heap is by consecutive insertions, producing O(n logn). This can be improved to O(n) by filling in the heap arbitrarily and performing recursive heapify until the properties of the min heap are satisified.
- Time complexity of deletion (in this case the root) is O(logn), due to traversal of the last node down the height of the tree until properties are satisfied.
- Deletion is performed 2n-1 times, due to re-insertion (O logn) of a new node after deletion of 2 nodes. So, O(logn \* 3n-1), giving O(n logn) time complexity to build the Huffman tree.
- Encoding the data involves depth first traversal of the Huffman tree, which is O(log n).
- Decoding the encoded data requires traversal of the tree n times, giving a time complexity of (n logn)
- The overall time complexity of the solution is the largest of the above time complexities, which is O(n logn).

### Design choices

- A min heap was chosen to implement the priority queue because it provides faster sorting after each iteration of building the Huffman tree. If a linked list was used, time complexity of insertion and deletion would be O(n). Instead with a heap this is achieved at O(log n).
- The heap nodes are implemented without requiring the use of children (these only become used in the Huffman tree, which use the same nodes for simplicity and saving space). Due to the properties of a min heap, that is, it is always complete, then the tree can be mapped into an array, where the indices of each node is known, as are the children and parent indices of each node given an index. Using an array to represent the heap speeds up heapify after insertion and deletion.
- Timestamps were implemented to ensure First In First Out (FIFO) property is maintained for nodes of equal frequency.
