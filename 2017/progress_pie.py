#!/usr/bin/env python
# coding=utf-8
# Copyright 2017 Brandon LeBlanc <demosdemon@gmail.com>

import sys
import math
import collections

Point = collections.namedtuple('Point', 'x y')


class Screen(object):
    def __init__(self, percentage=0):
        self.percentage = percentage

    @property
    def vector(self):
        if self.percentage == 0 or self.percentage == 100:
            return (50, 100)

        angle = (2 * math.pi * (self.percentage / 100.0)) * -1

        return Point(
            -50 * math.sin(angle) + 50,
            50 * math.cos(angle) + 50
        )

    def contains(self, point):
        if self.percentage == 0:
            return False
        if self.percentage == 100:
            return True

        if (point.x - 50) ** 2 + (point.y - 50) ** 2 > (50 ** 2):
            return False

        def point_in(a, b, c, p):
            def sign(a, b, c):
                return (a.x - c.x) * (b.y - c.y) - (b.x - c.x) * (a.y - c.y)

            x = sign(p, a, b) < 0.0
            y = sign(p, b, c) < 0.0
            z = sign(p, c, a) < 0.0

            return ((x == y) and (y == z))

        vector = self.vector

        # if vector.x != 50:
        #     m = (vector.y - 50.0) / (vector.x - 50.0)
        #     vector = Point(vector.x + 50, (vector.x + 50) * m)

        if self.percentage <= 50:
            return point_in(
                Point(50, 50),
                Point(50, 100),
                vector,
                point)
        else:
            return not point_in(
                Point(50, 100),
                Point(50, 50),
                vector,
                point)


def read_input(fd):
    T = int(next(fd))

    for _ in range(T):
        line = next(fd)
        percent, x, y = line.split()
        yield (Screen(int(percent)), Point(int(x), int(y)))


def main():
    with open(sys.argv[1]) as fd:
        for num, (screen, point) in enumerate(read_input(fd)):
            color = 'black' if screen.contains(point) else 'white'
            print('Case #{num}: {color}'.format(num=num + 1, color=color))


if __name__ == '__main__':
    main()
