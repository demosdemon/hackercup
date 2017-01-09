#!/usr/bin/env python
# coding=utf-8
# Copyright 2017 Brandon LeBlanc <demosdemon@gmail.com>

import sys
import math


def load_input(fp):
    days = int(next(fp))
    for _ in range(days):
        items = int(next(fp))

        array = [int(next(fp)) for _ in range(items)]

        yield sorted(array)


def process_input(array):
    trips = 0
    while array:
        last = array.pop()
        need = int(math.ceil(50.0 / last)) - 1
        array = array[need:]
        if array and array[-1] * len(array) < 50:
            array = []

        trips += 1

    return trips


def main(fp):
    if fp is None or fp == '-':
        fp = sys.stdin
    elif not hasattr(fp, 'read'):
        fp = open(fp)

    try:
        for num, array in enumerate(load_input(fp)):
            print('Case #{num}: {res}'.format(num=num + 1, res=process_input(array)))
    finally:
        fp.close()


if __name__ == '__main__':
    fp = sys.argv[1:2]
    if fp:
        main(fp[0])
    else:
        main(None)
