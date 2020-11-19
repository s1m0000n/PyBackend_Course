import implementations as impls
import cProfile, pstats, io


def test(f, n):
    pr = cProfile.Profile()
    pr.enable()
    f(n)
    pr.disable()
    print(f'{f.__name__}')
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

if __name__ == '__main__':
    print(f'Testing all on 30\n')
    test(impls.climb_stairs, 30)
    test(impls.climb_stairs2, 30)
    test(impls.climb_stairs3, 30)
    print('Testing efficient on 100_000\n')
    test(impls.climb_stairs2, 100_000)
    test(impls.climb_stairs3, 100_000)
    print('Testing efficient on 500_000\n')
    test(impls.climb_stairs2, 500_000)
    test(impls.climb_stairs3, 500_000)