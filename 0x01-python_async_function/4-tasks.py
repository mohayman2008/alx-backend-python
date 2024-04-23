#!/usr/bin/env python3
'''This script contains the definition for the function "task_wait_n"'''
import asyncio
from typing import List

task_wait_random = __import__("3-tasks").task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''This asynchronous function takes two integers <n> and <max_delay>,
    and generate tasks by calling task_wait_random() <n> times
    with <max_delay> as input parameter, runs the tasks asynchronously and
    returns a list of each task completion time'''
    tasks_list = tuple(task_wait_random(max_delay) for i in range(n))
    delays: List[float] = await asyncio.gather(*tasks_list)
    return sorted(delays)
