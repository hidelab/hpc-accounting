#!/usr/bin/env python3

import os
import sys

def queue_rows():
    """
    An iterator that yields each row of the accounting file that
    matches the queue.
    Each row is split at each ':' and yielded as a list.
    """

    accounting_file = os.environ.get('ACCOUNTING',
      'hidelab.accounting')
    queue = os.environ.get('QUEUE', 'hidelab.q')

    with open(accounting_file) as inp:
        for line in inp:
            row = line.split(':')
            if row[:1] != [queue]:
                continue
            yield row


def main():
    cpu_total = sum(
        float(row[13]) + float(row[34]) for row in queue_rows())

    mem_total = sum(float(row[37]) for row in queue_rows())

    first = float('inf')
    last = -float('inf')
    for row in queue_rows():
        if float(row[9]) == 0.0:
            continue
        first = min(first, float(row[9]))
        last = max(last, float(row[10]))
    elapsed = last - first

    print("cpu total", cpu_total)
    print("mem total", mem_total)
    print("elapsed", elapsed)
      

if __name__ == '__main__':
    main()
