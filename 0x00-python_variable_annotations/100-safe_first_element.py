#!/usr/bin/env python3
'''This script contains the definition for the function "safe_first_element"
'''
from typing import Optional, Sequence, Any


def safe_first_element(lst: Sequence[Any]) -> Optional[Any]:
    '''Dummy function to annotate'''
    if lst:
        return lst[0]
    else:
        return None
