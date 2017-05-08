#!/usr/bin/env python3

import itertools
import os
import sys

"""
Analyse a SGE accounting file.
See accounting(5) for column details,
but note that Python uses 0-based indexing,
whereas that man page uses 1-based indexing.
"""

class Statistic:
    """Structure to hold accumulated and computed statistics."""

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

def all_rows():
    accounting_file = os.environ.get('ACCOUNTING',
      'hidelab.accounting')

    with open(accounting_file) as inp:
        for line in inp:
            row = line.split(':')
            yield row

def main():
    cpu_total = sum(
        float(row[13]) * float(row[34]) for row in queue_rows())

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
    print("Total elapsed time in analysis period", elapsed)
    print()

    print("mean cores utilised", cpu_total/elapsed)
    print("mean mem", mem_total/elapsed)
    print()

    wait_time = dict()
    vmem = dict()
    cpu = dict()

    # This sorts by queue name (because that's the first element).
    rows = sorted(all_rows())
    # Remove rows that do not have valid wait times
    # (scheduler errors and similar leave 0 in submission_time
    # and start_time columns).
    rows = (row for row in rows if float(row[8]) and float(row[9]))

    qstat = dict()

    # Split by queue.
    # Accumulate statistics for each queue,
    # storing one Statistic() instance in the `qstat` dict
    # for each queue.
    for q, jobs in itertools.groupby(rows, lambda r: r[0]):
        jobs = list(jobs)
        stat = Statistic()
        qstat[q] = stat
        stat.wait_time = sum(float(row[9]) - float(row[8]) for
          row in jobs)
        stat.n = len(jobs)
        stat.vmem = (sum(float(row[42]) for row in jobs) /
          sum(bool(float(row[42])) for row in jobs))
        stat.cpu = sum(float(row[13]) * float(row[34]) for row in jobs)

    print("mean cores\twait\tMem(GB)\tn\tqueue")
    for q,stat in qstat.items():
        print(q,
              "{:.1f}".format(stat.cpu/elapsed),
              "{:.0f}".format(stat.wait_time/stat.n),
              "{:.2f}".format(stat.vmem/1e9),
              "{}".format(stat.n),
              sep='\t'
              )
      

if __name__ == '__main__':
    main()
