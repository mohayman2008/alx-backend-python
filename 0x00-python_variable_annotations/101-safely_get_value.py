#!/usr/bin/env python3
'''This script contains the definition for the function "safe_first_element"
'''
from typing import Optional, Union, TypeVar, Mapping, Any

T = TypeVar('T')


def safely_get_value(dct: Mapping,
                     key: Any,
                     default: Optional[T] = None) -> Union[Any, T]:
    '''Dummy function to annotate'''
    if key in dct:
        return dct[key]
    else:
        return default
