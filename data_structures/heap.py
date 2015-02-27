class Heap(object):

    def __init__(self):
        self.heap = [None]
        self.size = 1

    def insert(self, value):
        self.heap.append(value)
        self._swim(self.size)
        self.size += 1

    def pop(self):
        self._swap(1, -1)
        value = self.heap.pop()
        self.size -= 1
        self._sink(1)
        return value

    def _swim(self, index):
        parent = self._parent(index)
        if parent and self.heap[parent] < self.heap[index]:
            self._swap(index, parent)
            self._swim(parent)

    def _sink(self, index):
        child = self._max_child(index)
        if child:
            self._swap(index, child)
            self._sink(child)

    def _max_child(self, index):
        left, right = 2 * index, 2 * index + 1
        if left >= self.size:  # Left and right children don't exist
            return None
        if right >= self.size:  # Right child doesn't exists
            return left
        return left if self.heap[left] >= self.heap[right] else right

    def _parent(self, index):
        return index / 2

    def _swap(self, child, parent):
        self.heap[child], self.heap[parent] = self.heap[parent], self.heap[child]


if __name__ == '__main__':
    heap = Heap()
    heap.insert(9)
    heap.insert(1)
    heap.insert(3)
    heap.insert(10)
    heap.insert(11)
    heap.insert(15)
    heap.insert(15)
    heap.insert(7)
    heap.insert(12)
    heap.insert(25)
    heap.insert(13)
    heap.insert(5)
    print heap.pop()
    print heap.heap
    print heap.pop()
    print heap.heap
    print heap.pop()
    print heap.heap
    print heap.pop()
    print heap.heap
    print heap.pop()
    print heap.heap
