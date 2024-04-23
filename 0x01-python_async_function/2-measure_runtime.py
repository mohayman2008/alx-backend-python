#!/usr/bin/env python3
'''This script contains the definition for the function "measure_time"'''
import asyncio
from time import perf_counter

wait_n = __import__("1-concurrent_coroutines").wait_n


def measure_time(n: int, max_delay: int) -> float:
    '''This asynchronous function takes two integers <n> and <max_delay>,
    calls wait_n(n, max_delay) to run <n> tasks, and measures the average
    execution time per task'''
    initial = perf_counter()
    asyncio.run(wait_n(n, max_delay))
    total = perf_counter() - initial
    return total / n
