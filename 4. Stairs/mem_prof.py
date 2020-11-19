from functools import reduce
from memory_profiler import profile


@profile()
def slow(x):
    return climb_stairs(x)


def climb_stairs(n: int) -> int:
    return 1 if n in (0, 1) else climb_stairs(n - 1) + climb_stairs(n - 2)


@profile()
def climb_stairs2(n: int) -> int:
    return sum(reduce(lambda t, _: (t[1], t[0] + t[1]), range(2, n + 1), (0, 1)))


@profile()
def climb_stairs3(n: int) -> int:
    prev = 0
    cur = 1
    for _ in range(1, n + 1):
        prev_prev = prev
        prev = cur
        cur = prev + prev_prev
    return cur


if __name__ == '__main__':
    slow(30)
    # climb_stairs2(100_000)
    # climb_stairs3(100_000)
