#!/usr/bin/env python3
'''This script contains the definition for the coroutine "async_comprehension"
'''
import asyncio
from typing import List

async_generator = __import__("0-async_generator").async_generator


async def async_comprehension() -> List[float]:
    '''This coroutine collects 10 random numbers using async
    list comprehension over async_generator, then return the 10 random numbers
    '''
    return [n async for n in async_generator()]
