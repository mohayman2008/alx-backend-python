#!/usr/bin/env python3
'''This script contains the definition for the function "element_length"'''
from typing import List, Tuple, Iterable, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''This function takes an iterable of sequences and returns a list of
    tuples where each tuple contains a sequence from the input iterable
    and its length'''
    return [(i, len(i)) for i in lst]
