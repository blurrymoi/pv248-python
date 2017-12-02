import unittest as ut
from numpy import linalg
from math import factorial
from itertools import permutations


def volume(*args):  #, **kwargs):
    '''
    Pick one of the (n+1) points of an n-simplex.
    Subtract it from others to get n vectors.
    Put vectors into column of nxn matrix.
    (Volume of an n-parallelotope is the determinant.
    Divide by n! to get n-simplex volume.)
    '''
    pt = args[0]
    matrix = []
    if len(pt) != len(args) - 1:
        raise ValueError("not a simplex")
    for point in args[1:]:
        if len(point) != len(pt):
            raise ValueError("# of coords doesn't match in all points")
        matrix.append([a-b for (a, b) in zip(point, pt)])
    return abs( linalg.det(matrix) / factorial(len(args)-1) )


class TestVolume(ut.TestCase):

    def test_2d(self):
        """3 points, 2 components"""
        for a, b, c in permutations([[0, 0], [3, 0], [3, 4]]):
            self.assertEqual(volume(a, b, c), 6)

        self.assertEqual(volume([-2, -3], [-4, -3], [-2, -5]), 2)

    def test_3d(self):
        self.assertEqual(volume([0, 0, 0], [2, 0, 0], [2, 0, 2], [2, 3, 0]), 2)

    def test_too_few(self):
        with self.assertRaises(ValueError) as exe:
            volume([0, 0], [0, 3], [4])
            self.assertEqual(exe.exception, "# of coords doesn't match in all points")

    def test_too_many(self):
        with self.assertRaises(ValueError) as exe:
            volume([0, 0], [0, 1, 3], [4, 2])
            self.assertEqual(exe.exception, "# of coords doesn't match in all points")

    def test_dimensions(self):
        with self.assertRaises(ValueError) as exe:
            volume([0, 0], [4, 2])
            self.assertEqual(exe.exception, "not a simplex")

if __name__ == '__main__':
    ut.main()
