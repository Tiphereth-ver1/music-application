from collections import deque
from typing import Generic, Iterable, TypeVar

T = TypeVar('T')  # generic type variable

class FastQueue(Generic[T]):
    '''To rebuild later with proper pointer management.
    FastQueue is an implementation of a queue with additional indexing, to improve the performance of queues with operations not normally associated with them (get, insert, remove)'''
    def __init__(self):
        self._deque = deque()
        self._index = []
    
    def append(self, item: T) -> None:
        self._deque.append(item)
        self._index.append(item)
    
    def appendleft(self,item: T) -> None:
        self._deque.appendleft(item)
        self._index.insert(0, item)
        
    def popleft(self) -> T:
        song = self._deque.popleft()
        self._index.pop(0)
        return song

    def get(self, idx) -> T:
        return self._index[idx]

    def remove(self, item : T) -> None:
        self._deque.remove(item)
        self._index.remove(item)
    
    def size(self) -> int:
        return len(self._index)
    
    def extend(self, iterable: Iterable[T]):
        self._deque.extend(iterable)
        self._index.extend(iterable)

    def copy(self):
        
    
    def insert(self, pos: int, item: T) -> None:
        self._index.insert(pos, item)       # O(n)
        self._deque = deque(self._index)    # rebuild deque
    
    def __iter__(self):
        return iter(self._deque)

    def __contains__(self, item: T) -> bool:
        return item in self._deque
