#!/usr/bin/env python3
'''This script contains the definition for the function "wait_n"'''
from asyncio import as_completed

wait_random = __import__("0-basic_async_syntax").wait_random


async def wait_n(n: int, max_delay: int) -> float:
    '''This asynchronous function takes two integers <n> and <max_delay>,
    and calls wait_random() <n> times with <max_delay> as input parameter'''
    delays: [float] = []
    for delay in as_completed([wait_random(max_delay) for i in range(n)]):
        delays.append(await delay)
    return delays