#!/usr/bin/env python
# coding=utf-8
# Copyright 2017 Brandon LeBlanc <demosdemon@gmail.com>

import sys
import re
from scipy.misc import comb


class Dice(object):
    def __init__(self, string):
        match = re.match(r'^(?P<times>\d{1,2})d(?P<sides>\d{1,2})(?P<offset>[+-]\d{1,5})?$', string)
        if not match:
            raise ValueError('%s does not match expected format XdY[+-Z]')

        self.times = int(match.group('times'))
        self.sides = int(match.group('sides'))
        self.offset = int(match.group('offset') or 0)

    def __str__(self):
        return '{times}d{sides}{offset}'.format(
            times=self.times,
            sides=self.sides,
            offset='{:+d}'.format(self.offset) if self.offset else ''
        )

    def __repr__(self):
        return '{klass}({value!r})'.format(
            klass=self.__class__.__name__,
            value=str(self)
        )

    def probability(self, damage):
        min_roll = self.offset + (1 * self.times)
        max_roll = self.offset + (self.sides * self.times)

        if damage > max_roll:
            return 0

        if damage <= min_roll:
            return 1

        return sum(
            P(n, self.times, self.sides)
            for n in range(
                self.times,
                (self.sides * self.times) + 1)
            if (n + self.offset) >= damage
        ) / float(self.sides ** self.times)


def P(points, dice, sides):
    # default = lambda: collections.defaultdict(int)
    # table = collections.defaultdict(default)
    # for j in range(sides + 1):
    #     table[1][j] = 1
    #
    # for i in range(2, dice + 1):
    #     for j in range(1, points + 1):
    #         for k in range(1, min(sides + 1, j)):
    #             table[i][j] += table[i - 1][j - k]
    #
    # return float(table[dice][points])
    res = 0
    k_max = (points - dice) // sides
    for k in range(int(k_max) + 1):
        step = ((-1) ** k) * comb(dice, k) * comb(
            points - k * sides - 1,
            dice - 1)
        res += step
    return res


def load_input(fp):
    T = int(next(fp))

    for _ in range(T):
        # S, the number of spells is unecessary in python
        H, _ = tuple(map(int, next(fp).split()))
        dice = tuple(map(Dice, next(fp).split()))

        yield H, dice


def process_input(health, dice):
    max_roll = max(d.probability(health) for d in dice)
    return max_roll


def main(fp):
    if fp is None or fp == '-':
        fp = sys.stdin
    else:
        if not hasattr(fp, 'read'):
            fp = open(fp)

    try:
        for num, (health, dice) in enumerate(load_input(fp)):
            print('Case #{num}: {res:.6f}'.format(
                num=num + 1,
                res=process_input(health, dice)
            ))
    finally:
        if fp != sys.stdin:
            fp.close()


if __name__ == '__main__':
    fp = sys.argv[1:2]
    if fp:
        fp = fp[0]

    main(fp)
