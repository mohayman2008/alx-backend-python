#!/usr/bin/env python3
'''This script contains the definition for the function "wait_random"'''
import asyncio
from random import uniform


async def wait_random(max_delay: int = 10) -> float:
    '''This asynchronous function takes an integer <max_delay>, waits for
    random delay time between 0 and <max_delay> then returns that random
    delay value'''
    delay = uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
