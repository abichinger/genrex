from typing import List, Union, Tuple, Generator
import random
from collections import namedtuple

RangeArgs = Union[Tuple[int, int], Tuple[str, str]]
BracketMatch = namedtuple("BracketMatch", ["start", "stop", "level"])
CharMatch = namedtuple("CharMatch", ["index", "level"])

class MultiRange():

    def __init__(self, ranges:List[range]=[]):
        self.ranges = self._clean(ranges)

    def append(self, r):
        self.ranges = self._clean(self.ranges+[r])

    def _clean(self, ranges) -> List[range]:
        '''sort ranges and remove duplicates'''
        ranges = list(ranges)
        ranges.sort(key=lambda r: r.start)

        cleaned = []
        for r in ranges:
            if len(cleaned) == 0:
                cleaned.append(r)
            else:
                last_r = cleaned[-1]
                if r.stop <= last_r.stop:
                    continue
                elif r.start >= last_r.stop:
                    cleaned.append(r)
                elif r.start < last_r.stop:
                    cleaned.append(range(last_r.stop, r.stop))
        
        return cleaned

    def random_choice(self) -> int:
        i = random.randint(0, len(self)-1)
        return self[i]

    def __getitem__(self, index:int):
        for r in self.ranges:
            if index < len(r):
                return r[index]
            else:
                index -= len(r)
        raise IndexError()

    def __len__(self) -> int:
        length = 0
        for r in self.ranges:
            length += len(r)
        return length

    def inverted(self, start:int, stop:int) -> 'MultiRange':
        new_ranges = []
        for r in self.ranges:
            if start >= r.start:
                start = r.stop
            elif start < r.start and r.start < stop:
                new_ranges.append(range(start, r.start))
                start = r.stop
            elif start < r.start and r.start > stop:
                new_ranges.append(range(start, stop))
            
            if start >= stop:
                break

        if start < stop:
            new_ranges.append(range(start, stop)) 
            
        return MultiRange(new_ranges)

def multirange(*range_args:List[RangeArgs]) -> MultiRange:
    ranges = []
    for [start, stop] in range_args:
        if type(start) == str:
            start = ord(start)
        if type(stop) == str:
            stop = ord(stop)+1
        ranges.append(range(start, stop))
    return MultiRange(ranges)

def char_range(start:str, stop:str) -> range:
    return range(ord(start), ord(stop)+1)


def find_brackets(s, ob='(', cb=')') -> Generator[BracketMatch, None, None]:
    stack = []

    for i, c in enumerate(s):
        if c == ob:
            stack.append(i)
        elif c == cb:
            yield BracketMatch(stack.pop(), i, len(stack))

    if stack:
        raise IndexError('too many opening brackets')

def find_char(s:str, search:str, level_up="([", level_down="])"):
    stack = []
    for i, c in enumerate(s):
        if c in level_up:
            stack.append(i)
        elif c in level_down:
            stack.pop()
        elif c == search:
            yield CharMatch(index=i, level=len(stack))


