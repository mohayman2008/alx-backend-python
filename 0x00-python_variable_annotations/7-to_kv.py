#!/usr/bin/env python3
'''This script contains the definition for the function "to_kv"'''
from typing import List, Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    '''This function takes a string and an integer or float and
    returns a tuple'''
    return (k, v ** 2)
