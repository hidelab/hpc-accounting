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

def all_rows():
    accounting_file = os.environ.get('ACCOUNTING',
      'hidelab.accounting')

    with open(accounting_file) as inp:
        for line in inp:
            row = line.split(':')
            yield row

def main():
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

        first = min(float(row[9]) for row in jobs)
        last = max(float(row[10]) for row in jobs)
        stat.elapsed = last-first

        stat.wait_time = sum(float(row[9]) - float(row[8]) for
          row in jobs)
        stat.n = len(jobs)
        stat.vmem = (sum(float(row[42]) for row in jobs) /
          sum(bool(float(row[42])) for row in jobs))
        stat.cpu = sum(float(row[13]) * float(row[34]) for row in jobs)

    print("cores\twait\tMem(GB)\tn\tqueue")
    for q,stat in qstat.items():
        print(
            "{:.1f}".format(stat.cpu/stat.elapsed),
            "{:.0f}".format(stat.wait_time/stat.n),
            "{:.2f}".format(stat.vmem/1e9),
            "{}".format(stat.n),
            q,
            sep='\t'
        )
      

if __name__ == '__main__':
    main()
