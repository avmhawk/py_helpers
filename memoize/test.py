# encoding: utf-8
import unittest
import time
from memoize import memoize_with_params


class TestMemoizeFunction(unittest.TestCase):
    def test_functions_with_different_args(self):
        @memoize_with_params()
        def test_func(a, b, c):
            # для интов <= 256 питон кэширует значения:
            const = 1234
            res = const + sum([a, b, c])
            return res

        # functools wrapper должен сохранить оригинальное название обертываемой ф-ции:
        self.assertEqual(test_func.__name__, 'test_func')
        # func with args:
        self.assertEqual(id(test_func(2, 3, 4)), id(test_func(2, 3, 4)))
        self.assertFalse(id(test_func(2, 3, 4)) == id(test_func(2, 3, 5)))

        # kwargs:
        self.assertEqual(id(test_func(a=2, b=3, c=4)), id(test_func(a=2, b=3, c=4)))

    def test_cache_size_and_time_restrictions(self):
        @memoize_with_params(max_size=2)
        def test_func(*args):
            return sum([a + 1000 for a in args])

        first_cached_id = id(test_func(1, 2, 0))
        self.assertEqual(first_cached_id, id(test_func(1, 2, 0)))

        for x in range(11):
            test_func(1, 2, x)
        self.assertFalse(first_cached_id == id(test_func(1, 2, 0)))

        @memoize_with_params(max_time=1)
        def test_func2(*args):
            return sum([a + 1000 for a in args])
        first_cached_id = id(test_func2(1, 2, 0))

        self.assertEqual(first_cached_id, id(test_func2(1, 2, 0)))
        time.sleep(1)
        self.assertFalse(first_cached_id == id(test_func2(1, 2, 0)))


if __name__ == '__main__':
    unittest.main()
