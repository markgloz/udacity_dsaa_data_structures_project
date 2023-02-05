

class LinkedListNode:
    def __init__(self, value) -> None:
        self.value = value
        self.next = None
    
    def __repr__(self) -> str:
        return f"{self.value}"


class LinkedList:
    def __init__(self, head = None) -> None:
        self.head = head
        self.length = 0

    def append(self, value) -> None:
        new_node = LinkedListNode(value)
        if not self.head:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1
    
    def search(self, value) -> bool:
        if not self.head:
            return False
        else:
            node = self.head
            while node:
                if node.value == value:
                    return True
                else:
                    node = node.next
            return False
    
    def __len__(self) -> int:
        return self.length
    
    def __repr__(self) -> str:
        repr_str = ""
        node = self.head
        while node:
            repr_str += f"{node} -> "
            node = node.next
        return repr_str[:-4]


def union(linked_list_1: LinkedList, linked_list_2: LinkedList) -> LinkedList:
    union_linked_list = LinkedList()
    node = linked_list_1.head
    while node:
        if not union_linked_list.search(node.value):
            union_linked_list.append(node.value)
        node = node.next
    node = linked_list_2.head
    while node:
        if not union_linked_list.search(node.value):
            union_linked_list.append(node.value)
        node = node.next
    if union_linked_list.head:
        return union_linked_list
    else:
        return None
    
def intersection(linked_list_1: LinkedList, linked_list_2: LinkedList) -> LinkedList:
    intersection_linked_list = LinkedList()
    node = linked_list_1.head
    while node:
        if not intersection_linked_list.search(node.value) and linked_list_2.search(node.value):
            intersection_linked_list.append(node.value)
        node = node.next
    if intersection_linked_list.head:
        return intersection_linked_list
    else:
        return None


# Tests 1 - Dev tests
array_1 = [1, 2, 3]
array_2 = [2, 3, 4, 5]
linked_list_1 = LinkedList()
linked_list_2 = LinkedList()

for v in array_1:
    linked_list_1.append(v)

for v in array_2:
    linked_list_2.append(v)

print(union(linked_list_1, linked_list_2))
print(intersection(linked_list_1, linked_list_2))

# Tests 2 - Udacity test

linked_list_1 = LinkedList()
linked_list_2 = LinkedList()

element_1 = [3,2,4,35,6,65,6,4,3,21]
element_2 = [6,32,4,9,6,1,11,21,1]

for i in element_1:
    linked_list_1.append(i)

for i in element_2:
    linked_list_2.append(i)

print(union(linked_list_1,linked_list_2))
print(intersection(linked_list_1,linked_list_2))

# Tests 3 - Udacity test

linked_list_3 = LinkedList()
linked_list_4 = LinkedList()

element_1 = [3,2,4,35,6,65,6,4,3,23]
element_2 = [1,7,8,9,11,21,1]

for i in element_1:
    linked_list_3.append(i)

for i in element_2:
    linked_list_4.append(i)

print (union(linked_list_3,linked_list_4))
print (intersection(linked_list_3,linked_list_4))
