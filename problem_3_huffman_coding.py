import sys


class Node:
    def __init__(self, frequency: int = None, character: str = None, left = None, right = None, timestamp = 0) -> None:
        self.frequency = frequency
        self.character = character
        self.left = left
        self.right = right
        self.timestamp = timestamp
    
    def has_child(self):
        if (self.left != None) or (self.right != None):
            return True
        else:
            return False
    
    def __repr__(self) -> str:
        return f"Node['{self.character}': {self.frequency}]"


class MinHeap:
    def __init__(self) -> None:
        self.heap = []
    
    def insert(self, node: Node) -> None:
        self.heap.append(node)
        self.heapify_up()
    
    def heapify_up(self) -> None:
        index = len(self.heap) - 1
        while index > 0:
            if self.get_node(index).frequency < self.get_parent(index).frequency:
                self.swap_nodes(index, self.get_parent_index(index))
                index = self.get_parent_index(index)
            elif self.get_node(index).frequency == self.get_parent(index).frequency:
                if self.get_node(index).timestamp < self.get_parent(index).timestamp:
                    self.swap_nodes(index, self.get_parent_index(index))
                    index = self.get_parent_index(index)
                else:
                    break
            else:
                break
    
    def dequeue(self) -> Node:
        if not self.heap:
            return None
        min_node = self.heap[0]
        if len(self.heap) > 1:
            self.heap[0] = self.heap.pop()
            self.heapify_down()
            return min_node
        else:
            return self.heap.pop()

    def heapify_down(self) -> None:
        index = 0
        while self.has_left_child(index):
            if self.has_right_child(index):
                if self.get_left_child(index).frequency < self.get_right_child(index).frequency:
                    min_child_index = self.get_left_child_index(index)
                elif self.get_left_child(index).frequency == self.get_right_child(index).frequency:
                    if self.get_left_child(index).timestamp < self.get_right_child(index).timestamp:
                        min_child_index = self.get_left_child_index(index)
                    else:
                        min_child_index = self.get_right_child_index(index)
                else:
                    min_child_index = self.get_right_child_index(index)
            else:
                min_child_index = self.get_left_child_index(index)
            if self.get_node(index).frequency > self.get_node(min_child_index).frequency:
                self.swap_nodes(index, min_child_index)
                index = min_child_index
            elif self.get_node(index).frequency == self.get_node(min_child_index).frequency:
                if self.get_node(index).timestamp > self.get_node(min_child_index).timestamp:
                    self.swap_nodes(index, min_child_index)
                    index = min_child_index
                else:
                    break
            else:
                break
            
    def peek(self) -> Node:
        if self.heap:
            return self.heap[0]
        else:
            return None
    
    def swap_nodes(self, index_1: int, index_2: int) -> None:
        node_2 = self.get_node(index_2)
        self.heap[index_2] = self.heap[index_1]
        self.heap[index_1] = node_2

    def get_left_child_index(self, index) -> int:
        return (index * 2) + 1

    def get_right_child_index(self, index) -> int:
        return (index * 2) + 2
    
    def get_parent_index(self, index) -> int:
        return (index - 1) // 2

    def has_left_child(self, index) -> bool:
        return self.get_left_child_index(index) < len(self.heap)
    
    def has_right_child(self, index) -> bool:
        return self.get_right_child_index(index) < len(self.heap)
    
    def has_parent(self, index) -> bool:
        return index > 0

    def get_node(self, index) -> Node:
        return self.heap[index]
    
    def get_left_child(self, index) -> Node:
        return self.heap[self.get_left_child_index(index)]
    
    def get_right_child(self, index) -> Node:
        return self.heap[self.get_right_child_index(index)]
    
    def get_parent(self, index) -> Node:
        return self.heap[self.get_parent_index(index)]
    
    def set_node(self, index, node) -> None:
        self.heap[index] = node

    def __repr__(self) -> str:
        return str(self.heap)
    
    def __len__(self) -> int:
        return len(self.heap)


class HuffmanTree:
    def __init__(self, root: Node = None) -> None:
        self.root = root
    
    def get_root(self) -> Node:
        return self.root
    
    def set_root(self, root) -> None:
        self.root = root


def depth_first_traversal(tree: HuffmanTree, codes: dict) -> str:
    root = tree.get_root()

    def recursive(node: Node, code: str):
        if node.has_child():
            code = recursive(node.left, code + '0')
            code = recursive(node.right, code + '1')
        else:
            codes[node.character]['code'] = code
        return code[:-1]
    
    recursive(root, '')
    return

def huffman_encoding(data):
    if data == '':
        return '', ''
    if data is None:
        return None, None
    codes = {}
    for char in data:
        if char not in codes:
            codes[char] = {'frequency': 1}
        else:
            codes[char]['frequency'] += 1
    priority_queue = MinHeap()
    timestamp = 0
    for char, parameters in codes.items():
        priority_queue.insert(Node(parameters['frequency'], char, timestamp=timestamp))
        timestamp += 1
    
    huffman_tree = HuffmanTree()
    if len(priority_queue) == 1:
        huffman_tree.set_root(priority_queue.dequeue())
    else:
        while len(priority_queue) > 1:
            node_1 = priority_queue.dequeue()
            node_2 = priority_queue.dequeue()
            freq_sum = node_1.frequency + node_2.frequency
            internal_node = Node(frequency = freq_sum, left = node_1, right = node_2, timestamp=timestamp)
            timestamp += 1
            huffman_tree.set_root(internal_node)
            priority_queue.insert(internal_node)
    
    # Perform a depth first traversal, similar to pre-order, to get binary codes
    depth_first_traversal(huffman_tree, codes)

    # Encode
    encoded_data = ''
    for char in data:
        encoded_data += codes[char]['code']
    
    return encoded_data, huffman_tree
        
def huffman_decoding(data, tree: HuffmanTree):
    if data == '':
        if tree == '':
            return ''
        else:
            return tree.get_root().character * tree.get_root().frequency
    if None in {data, tree}:
        return None
    decoded_data = ''
    node = tree.get_root()
    for bit in data:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        if not node.has_child():
            decoded_data += node.character
            node = tree.get_root()
    return decoded_data


if __name__ == "__main__":
    a_great_sentence = "The bird is the word"

    # print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    # print ("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    # print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    # print ("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    # print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    # print ("The content of the encoded data is: {}\n".format(decoded_data))

# Add your own test cases: include at least three test cases
# and two of them must include edge cases, such as null, empty or very large values

# Test Case 1
data = "AAAAAAABBBCCCCCCCDDEEEEEE"
encoded_data, tree = huffman_encoding(data)
decoded_data = huffman_decoding(encoded_data, tree)
assert decoded_data == data

# Test Case 2
data = 'Hello World'
encoded_data, tree = huffman_encoding(data)
decoded_data = huffman_decoding(encoded_data, tree)
assert decoded_data == data
# print(f"Size of original data: {sys.getsizeof(data)}, Size of encoded data: {sys.getsizeof(int(encoded_data, base=2))}, Size of decoded data: {sys.getsizeof(decoded_data)}")

# Test Case 3 - Null
null_data = None
null_encoded_data, null_tree = huffman_encoding(null_data)
null_decoded_data = huffman_decoding(null_encoded_data, null_tree)
assert null_decoded_data == null_data

# Test Case 4 - Empty
empty_data = ''
empty_encoded_data, empty_tree = huffman_encoding(empty_data)
empty_decoded_data = huffman_decoding(empty_encoded_data, empty_tree)
assert empty_decoded_data == empty_data

# Test Case 5
data = '42'
encoded_data, tree = huffman_encoding(data)
decoded_data = huffman_decoding(encoded_data, tree)
assert decoded_data == data
# print(f"Size of original data: {sys.getsizeof(data)}, Size of encoded data: {sys.getsizeof(int(encoded_data, base=2))}, Size of decoded data: {sys.getsizeof(decoded_data)}")

# Test Case 6 - Large
large_data = 'abcdefghijklmnopqrstuvABCDEFGHIJKLMNOPQRSTUVWXZY0123456789;"/.,$£@!^%(^)(&%`~\\' * (10 ** 2)
large_encoded_data, large_tree = huffman_encoding(large_data)
large_decoded_data = huffman_decoding(large_encoded_data, large_tree)
assert large_decoded_data == large_data
# print(f"Size of original data: {sys.getsizeof(large_data)}, Size of encoded data: {sys.getsizeof(int(large_encoded_data, base=2))}, Size of decoded data: {sys.getsizeof(large_decoded_data)}")

# Test Case 7
data = 'A'
encoded_data, tree = huffman_encoding(data)
decoded_data = huffman_decoding(encoded_data, tree)
assert decoded_data == data

# Test Case 8
data = 'AAAA'
encoded_data, tree = huffman_encoding(data)
decoded_data = huffman_decoding(encoded_data, tree)
assert decoded_data == data

# Print null, empty and large test results to meet project requirements
print(empty_decoded_data == empty_data) # Should print True
print(null_decoded_data == null_data) # Should print True
print(large_decoded_data == large_data) # Should print True
print(f"Size of original data: {sys.getsizeof(large_data)}, Size of encoded data: {sys.getsizeof(int(large_encoded_data, base=2))}, Size of decoded data: {sys.getsizeof(large_decoded_data)}")
# Above line should print: Size of original data: 7873, Size of encoded data: 6560, Size of decoded data: 7873