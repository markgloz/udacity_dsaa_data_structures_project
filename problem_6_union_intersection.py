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
    
    def sorted_append(self, value) -> None:
        new_node = LinkedListNode(value)
        if not self.head:
            self.head = new_node
            return
        if value < self.head.value:
            new_node.next = self.head
            self.head = new_node
            return
        node = self.head
        while node.next and value >= node.next.value:
            node = node.next
        new_node.next = node.next
        node.next = new_node
    
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
            union_linked_list.sorted_append(node.value)
        node = node.next
    node = linked_list_2.head
    while node:
        if not union_linked_list.search(node.value):
            union_linked_list.sorted_append(node.value)
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
            intersection_linked_list.sorted_append(node.value)
        node = node.next
    if intersection_linked_list.head:
        return intersection_linked_list
    else:
        return None

def test_answer(array_1: list, array_2: list, answer: LinkedList, type = 'Union'):
    set_1 = set(array_1)
    set_2 = set(array_2)
    solution_set = set_1.union(set_2) if type == 'Union' else set_1.intersection(set_2)
    if answer is None:
        if not solution_set:
            return True
        else:
            return False
    node = answer.head
    while node:
        if node.value not in solution_set:
            return False
        solution_set.remove(node.value)
        node = node.next
    if not solution_set:
        return True
    else:
        return False

# Tests 1 - Dev tests
array_1 = [1, 2, 3]
array_2 = [2, 3, 4, 5]
linked_list_1 = LinkedList()
linked_list_2 = LinkedList()

for v in array_1:
    linked_list_1.append(v)

for v in array_2:
    linked_list_2.append(v)

union_1 = union(linked_list_1, linked_list_2) # 1 -> 2 -> 3 -> 4 -> 5
assert test_answer(array_1, array_2, union_1, 'Union')
inter_1 = intersection(linked_list_1, linked_list_2) # 2 -> 3
assert test_answer(array_1, array_2, inter_1, 'Intersection')

# Tests 2 - Udacity test
linked_list_1 = LinkedList()
linked_list_2 = LinkedList()

element_1 = [3,2,4,35,6,65,6,4,3,21]
element_2 = [6,32,4,9,6,1,11,21,1]

for i in element_1:
    linked_list_1.append(i)

for i in element_2:
    linked_list_2.append(i)

union_2 = union(linked_list_1,linked_list_2) # 1 -> 2 -> 3 -> 4 -> 6 -> 9 -> 11 -> 21 -> 32 -> 35 -> 65
assert test_answer(element_1, element_2, union_2, 'Union')
inter_2 = intersection(linked_list_1,linked_list_2) # 4 -> 6 -> 21
assert test_answer(element_1, element_2, inter_2, 'Intersection')

# Tests 3 - Udacity test

linked_list_3 = LinkedList()
linked_list_4 = LinkedList()

element_1 = [3,2,4,35,6,65,6,4,3,23]
element_2 = [1,7,8,9,11,21,1]

for i in element_1:
    linked_list_3.append(i)

for i in element_2:
    linked_list_4.append(i)

union_3 = union(linked_list_3,linked_list_4) # 1 -> 2 -> 3 -> 4 -> 6 -> 7 -> 8 -> 9 -> 11 -> 21 -> 23 -> 35 -> 65
assert test_answer(element_1, element_2, union_3, 'Union')
inter_3 = intersection(linked_list_3,linked_list_4) # None
assert test_answer(element_1, element_2, inter_3, 'Intersection')

if __name__ == '__main__':
    print(union_1, inter_1, union_2, inter_2, union_3, inter_3, sep='\n')