#!/usr/bin/env python3
'''This script contains the definition for the coroutine "measure_runtime"'''
import asyncio
import time

async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime() -> float:
    '''This coroutine execute async_comprehension four times in parallel and
    measures the total runtime and return it.
    '''
    initial = time.perf_counter()
    await asyncio.gather(*tuple(async_comprehension() for _ in range(4)))
    return time.perf_counter() - initial
