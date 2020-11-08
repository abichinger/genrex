import random
from typing import List, Union
from genrex.util import multirange, MultiRange, char_range, find_brackets, find_char
from enum import Enum
import sys

class PatternBase():
    
    def random(self) -> str:
        index = random.randint(0, len(self)-1)
        return self[index]

    def __getitem__(self, index:int) -> str:
        pass

    def __len__(self) -> int:
        pass
        
class Char(PatternBase): 
    
    def __init__(self, char:int):
        self.char = chr(char)

    def random(self) -> str:
        return self.char

    def __getitem__(self, index:int) -> str:
        if index != 0:
            raise IndexError
        return self.char

    def __len__(self) -> int:
        return 1

class Set():

    def __init__(self, multi_range:Union[range, MultiRange]):
        self.multi_range = multi_range

    def __getitem__(self, index:int) -> str:
        return chr(self.multi_range[index])

    def __len__(self) -> int:
        return len(self.multi_range)

    def inverted(self, start:int, stop:int) -> int:
        return Set(self.multi_range.inverted(start, stop))

    def append(self, r):
        self.multi_range.append(r)
    
class RepeatingPattern(PatternBase):
    
    def __init__(self, pattern:PatternBase, m:int, n:int):
        self.p = pattern
        self.m = m
        self.n = n

    def __getitem__(self, index:int) -> str:
        if index > len(self)-1:
            raise IndexError
 
        for m in range(self.m, self.n+1):
            l = len(self.p)**m
            if l > index:
                break
            else:
                index -= l

        item = ''
        for m in range(0, m):
            item += self.p[index%len(self.p)]
            index = int(index/len(self.p))

        return item

    def __len__(self) -> int:
        cardinality = 0
        for i in range(self.m, self.n+1):
            cardinality += len(self.p)**i
        return cardinality

class Pattern(PatternBase):

    def __init__(self, children:List[PatternBase]):
        self.children = children

    def append(self, child):
        self.children.append(child)

    def __getitem__(self, index:int) -> str:
        if index > len(self)-1:
            raise IndexError

        item = ''
        for child in self.children:
            item += child[index%len(child)]
            index = int(index/len(child))
        return item

    def __len__(self) -> int:
        cardinality = 1
        for child in self.children:
            child_len = len(child)
            if child_len > 0:
                cardinality *= child_len
        
        return cardinality

class Either(PatternBase):

    def __init__(self, a:PatternBase, b:PatternBase):
        self.a = a
        self.b = b
    
    def __getitem__(self, index:int) -> str:
        if index < len(self.a):
            return self.a[index]
        else:
            return self.b[index-len(self.a)]

    def __len__(self) -> int:
        return len(self.a) + len(self.b)


import sre_parse
from sre_constants import *

def parse(pattern:str, flags=0, max_depth=15) -> PatternBase:
    '''parses a regular expression using the built in sre engine
    
    :param pattern: re-style regular expression
    :param flags: re flags
    :param max_depth: limit of repeating expressions
    '''

    p = sre_parse.parse(pattern)
    return _parse(p, flags, max_depth)

def _parse(p:sre_parse.SubPattern, flags, max_depth):

    subp = Pattern([])

    for op, av in p.data:
        if op is LITERAL:
            subp.append(Char(av))
        if op is IN:
            char_set = Set(MultiRange())
            for op, a in av:
                if op is RANGE:
                    char_set.append(range(a[0], a[1]+1))
                if op is LITERAL:
                    char_set.append(range(a, a+1))
            subp.append(char_set)
        if op is SUBPATTERN:
            subp.append(_parse(av[-1], flags, max_depth))
        if op is BRANCH:
            branches = av[-1]
            a = _parse(branches[0], flags, max_depth)
            for b in branches[1:]:
                a = Either(a, _parse(b, flags, max_depth))
            subp.append(a)
        if op is MAX_REPEAT or op is MIN_REPEAT:
            a = _parse(av[-1], flags, max_depth)
            if av[1] is MAXREPEAT:
                subp.append(RepeatingPattern(a, av[0], max_depth))
            else:
                subp.append(RepeatingPattern(a, av[0], av[1]))
        if op is ANY:
            new_line = Set(MultiRange([range(ord('\n'), ord('\n')+1)]))
            subp.append(new_line.inverted(0, sys.maxunicode))

    return subp