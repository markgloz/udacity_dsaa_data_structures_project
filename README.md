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

- Space complexity is O(1). The cache remains at a fixed length regardless of input data size.

### Design choices

- A python dictionary was chosen over implementing a hash map from scratch. This was done both primarily for simplicity.
- If a hash map were to be implemented, the hash function would generate a bucket index using by summing a prime-number based product of the Unicode character encoding for a given str(key). The index would feed into a bucket array.
- Collisions could be handled through separate chaining.
- The time complexity on average for adding and removing items to this implemented hash map would be on average O(1), depending on the initial array size and load factor chosen.
- Python's SipHash hash function for dictionaries has good performance characteristics and rarely encounters collisions out of the box, causing the practical time order to be closer to O(1) than perhaps the hash function discussed prior.

## Problem 2: File recursion

### Efficiency

- Time complexity is related to the number of subdirectories and files contained within the path given.
- It is linear time complexity, O(n), where n represents the number of unique subpaths in the given path.
- The base case of the solution is if the path being evaluated is a file, then it returns the path of that file.
- The recursive case is if the path being evaluated is a directory.

- Space complexity is related to the depth of recursion, O(n), where n is the number of levels of subdirectories.

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

- Space complexity is O(n)
- Adding nodes to the minheap is O(n) in space complexity.
- For k nodes in the Huffman tree, the space complexity is O(k).
- Decoding produces the input string, therefore is O(n)

### Design choices

- A min heap was chosen to implement the priority queue because it provides faster sorting after each iteration of building the Huffman tree. If a linked list was used, time complexity of insertion and deletion would be O(n). Instead with a heap this is achieved at O(log n).
- The heap nodes are implemented without requiring the use of children (these only become used in the Huffman tree, which use the same nodes for simplicity and saving space). Due to the properties of a min heap, that is, it is always complete, then the tree can be mapped into an array, where the indices of each node is known, as are the children and parent indices of each node given an index. Using an array to represent the heap speeds up heapify after insertion and deletion.
- Timestamps were implemented to ensure First In First Out (FIFO) property is maintained for nodes of equal frequency.

## Problem 4: Active Directory

### Efficiency

- Time complexity is O(n) in the worst case, where n is the total number of groups contained within the parent, recursively.
- Each group is checked in the order in which they were appended until a group is found that contains the username.
- In the worst case, every group could be checked and False returned as the username was not found.

- Space complexity is proportional to the recursion depth in the call stack. This is determined by the number of subfolders within the root, n. In this case, space complexity is O(n).

### Design choices

- A recursive function was chosen as each group can be treated as a branch, which must be traversed until the username is found in that branch, or not.
- Branches can branch out of branches, and the users can be thought of as leaves.
- So the function is checking the leaves (users) on each branch, traversing in the order at which the parent subchild groups were added.
- If the base case is hit, True is recursively returned until the parent is reached.
- This was chosen over a loop, where it would be more difficult to return to the parents recursively after searching through each branch. It would likely need variable(s) storing the previous group, which takes up more space.

## Problem 5: Blockchain

### Efficiency

- If difficulty is ignored (i.e. no proof of work), time complexity of adding a block is O(1).
- Time complexity is heavily skewed by the proof of work if difficulty > 0 and it is not possible to calculate.
- The time to compute the proof of works increases with a number of factors, including the difficulty (How many leading zeros must there be in the resulting hash by changing the nonce value).
- Time complexity also increases with the data input size. A larger string increases the time required to find the correct nonce value. The current implementation simply starts at 0 and increments by 1 on each iteration.
- When a block is mined, it is added to the blockchain. This is primarily implemented through a linked list, updating the head on each successful mine, which contains a link to the previous block. After proof of work, adding to the blockchain is done in constant time O(1).
- A hashmap is also created such that a search can be done to find a block given a key of the hash value. This makes this getter function constant time O(1).
- An array is also produced of the blockchain as a simple method to both know the length of the chain (which could also be done with a counter) and a way to print the entire blockchain. This could easily be changed to iterate through the linked list, both of these get the blocks in the blockchain in linear time, O(n).

- If difficulty is ignored, space efficiency is O(1). Hashing is done in constant space (256 bits) regardless of the input data.

### Design choices

- A simple but full blockchain was implemented as a REST API using Flask, and cURL requests can be made to interact with the app. Alternatively, the tests run locally with using Flask. Useful cURL commands can be found commented under `if __name__ == "__main__":`.
- The orders of operation were created in a way to be analogous to cryptocurrency blockchains.
  - User adds data to a pool of unverified data. This could be transactional data.
  - A miner then performs proof of work, finding the nonce value to produce a hash value that meets the difficulty requirements. Difficulty 2 means the hash must have 2 leading zeros.
  - Once the miner finds the hash, a request is made to add this to the blockchain. This succeeds if the previous hash noted in the block matches that in the records in the current blockchain. This is analogous to preventing malicious mutation of the blockchain.
  - If the hash also passes validation checks, such that the hash value of the block is correct and has the leading zeros requirement, it gets added to the block chain and removed from the unvalidated list.
  - An array was chosen for the unvalidated list for simplicity.
  - The chain can be accessed through an array, as a more suitable solution, or by a linked list (from the head node, traversing through the previous hashes using a hashmap), to more closely match the requirements of the project.

## Problem 6: Union and Intersection

### Efficiency

- Solution for both Union and Intersection is in linear time, O(n)
- LinkedList search is done in linear time, O(n)
- LinkedList append is done in constant time, O(1)
- LinkedList sorted_append is done in linear timee, O(n)
- Union performs a search and a sorted_append for each array, resulting in O(n)
- Intersection performs two searches and a sorted_append, resulting in O(n)

- Space efficiency is O(n) in the worst case. Linked list grows with input data.

### Design choices

- LinkedList append() was performed on converting the arrays to linked lists, done in constant time O(1)
- LinkedList sorted_append() was performed to produce the union and intersection LinkedLists to improve the readability of the output to the user, at the cost of linear over constant time complexity
