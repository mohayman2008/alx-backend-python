#!/usr/bin/env python3
'''This script contains the definition for the coroutine "async_generator"'''
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    '''This coroutine is a generator that asynchronously wait 1 second,
    then yield a random number between 0 and 10 and repeat that for 10 times
    '''
    for i in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
