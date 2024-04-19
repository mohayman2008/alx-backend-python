#!/usr/bin/env python3
'''This script contains the definition for the function "sum_mixed_list"'''
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    '''This function takes a mixed list of floats and integers and
    returns their sum'''
    return sum(mxd_lst)
