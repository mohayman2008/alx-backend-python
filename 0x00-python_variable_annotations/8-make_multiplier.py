#!/usr/bin/env python3
'''This script contains the definition for the function "make_multiplier"'''
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''This function takes a float <multiplier> and returns a function that
    multiplies a float by <multiplier>'''
    return lambda n: n * multiplier
