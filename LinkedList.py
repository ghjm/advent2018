class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self, init_data=None):
        self.head = None
        self.tail = None
        if init_data is not None:
            for data in init_data:
                node = Node(data)
                if self.head is None:
                    self.head = node
                    self.tail = node
                else:
                    node.prev = last_node
                    node.prev.next = node
                    self.tail = node

    def add(self, data, after=None):
        node = Node(data)
        if self.head is None:
            self.head = node
            self.tail = node
            node.next = None
            node.prev = None
        elif after is not None:
            node.next = after.next
            node.prev = after
            after.next = node
            if node.next is None:
                self.tail = node
            else:
                node.next.prev = node
        else:
            self.tail.next = node
            node.prev = self.tail
            node.next = None
            self.tail = node
        return node

    def forward_circular(self, node, steps):
        ptr = node
        for i in range(steps):
            if ptr.next is None:
                ptr = self.head
            else:
                ptr = ptr.next
        return ptr

    def backward_circular(self, node, steps):
        ptr = node
        for i in range(steps):
            if ptr.prev is None:
                ptr = self.tail
            else:
                ptr = ptr.prev
        return ptr

    def search(self, k):
        p = self.head
        if p is not None:
            while p.next is not None:
                if p.data == k:
                    return p				
                p = p.next
            if p.data == k:
                return p
        return None

    def remove(self, p):
        if p.prev is None:
            self.head = p.next
            self.head.prev = None
        else:
            p.prev.next = p.next
        if p.next is None:
            self.tail = p.prev
            self.tail.next = None
        else:
            p.next.prev = p.prev

    def __str__(self):
        l = list()
        p = self.head
        if p is not None:
            while p.next != None:
                l.append(p.data)
                p = p.next
            l.append(p.data)
        return str(l)

    def __len__(self):
        p = self.head
        i = 0
        while p is not None:
            i += 1
            p = p.next
        return i
