#!/usr/bin/env python3

import os
import sys

def main():
    accounting_file = os.environ.get('ACCOUNTING',
      'hidelab.accounting')
    queue = os.environ.get('QUEUE', 'hidelab.q')

    cpu_total = 0
    with open(accounting_file) as inp:
        for line in inp:
            row = line.split(':')
            if row[0] != queue:
                continue
            cpu_total += float(row[13]) * float(row[34])

    mem_total = 0
    with open(accounting_file) as inp:
        for line in inp:
            row = line.split(':')
            if row[0] != queue:
                continue
            mem_total += float(row[37])

    first = float('inf')
    last = -float('inf')
    with open(accounting_file) as inp:
        for line in inp:
            row = line.split(':')
            if row[0] != queue:
                continue
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
