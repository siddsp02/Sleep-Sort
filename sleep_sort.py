"""This is a sorting algorithm based on a Youtube comment
about an alternative to traditional sorting algorithms,
which is supposed to make sorting doable in linear runtime.
It was intended as a joke, but was in interesting idea to
implement.
"""


import asyncio
import random
import time
import sys


async def sleep_sort(array: list[int]) -> tuple[list[int], float]:
    """A coroutine (single-threaded) implementation of the "sleep sort"
    algorithm as well as a benchmark of the amount of time it takes.

    Arguments:
        array (list[int]): The array to sort.

    Returns:
        list[int]: The input array sorted in ascending order.
        int: The amount of time it took to execute the sort.
    """

    UNITS = 10 ** -9

    coroutines = []
    sorted_array = []

    async def sleep_append(value: int) -> None:
        await asyncio.sleep(UNITS * value)
        sorted_array.append(value)

    start = time.perf_counter()  # Start of benchmark.

    for value in array:
        coroutines.append(asyncio.create_task(sleep_append(value)))

    for coroutine in coroutines:
        await coroutine

    end = time.perf_counter()  # End of benchmark.

    return sorted_array, end - start


async def main(size: int, maximum: int) -> None:
    """The main thread in which the size of a generated array,
    as well as the maximum value of the integers within the array.

    Arguments:
        size (int): The size or length of the array.
        maximum (int): The maximum value of a number within the array.
    """
    old_array = [random.randint(0, maximum) for _ in range(size)]

    # Unpack the results of the coroutine call.
    new_array, elapsed = await asyncio.create_task(sleep_sort(old_array))

    # Use native Python sorting to compare results.
    old_array.sort()

    print(f"Sorted Array: {new_array}")
    print(f"Time: {elapsed:.4f}")
    print(f"Sorted: {new_array == old_array}")


if __name__ == "__main__":
    print("\nResults:\n")
    asyncio.run(main(int(sys.argv[1]), int(sys.argv[2])))
