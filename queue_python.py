import random

class QueuePython:
    def __init__(self):
        self._items = []
    
    def clear(self):
        self._items.clear()
    
    def enqueue(self, value):
        self._items.append(value)
    
    def dequeue(self):
        if not self._items:
            return 0, False
        return self._items.pop(0), True
    
    def peek(self):
        if not self._items:
            return 0, False
        return self._items[0], True
    
    def size(self):
        return len(self._items)
    
    def fill_random(self, count, min_val, max_val):
        for _ in range(count):
            self._items.append(random.randint(min_val, max_val))
    
    def get_all(self):
        return self._items.copy()