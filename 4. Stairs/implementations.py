from functools import reduce


def climb_stairs(n: int) -> int:
    return 1 if n in (0, 1) else climb_stairs(n - 1) + climb_stairs(n - 2)


def climb_stairs2(n: int) -> int:
    return sum(reduce(lambda t, _: (t[1], t[0] + t[1]), range(n - 1), (0, 1)))


def climb_stairs3(n: int) -> int:
    prev = 0
    cur = 1
    for _ in range(n):
        prev_prev = prev
        prev = cur
        cur = prev + prev_prev
    return cur
