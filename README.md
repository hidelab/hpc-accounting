# The hidelab queue on iceberg

The numbers here come from a report produced by running

```
    python bin/qtotal.py
```

The input is an extract made from the SGE accounting file.

Users of `hidelab.q`:

```
sh bin/who

fe1mpc
md1jck
md1wwxx
md1xdrj
md4zsa
mdp15cmg
```

(notably, not Gabriel)


## CPU Utilisation

1.7 cores on average on the period of analysis.
We rent a 16 core node, so this is about 10%

## RAM Utilisation

25.47 GB

(not sure what the reported number is here,
or what the average is over,
so interpret with caution).

## Wait time

Average wait time on `hidelab.q` is about 400 seconds.

## What we'd like to measure

Used Gigabyte seconds on `hidelab.q`:

Used CPU seconds on other queues:

Used Gigabyte seconds on other queues:

Average wait time on other queues:
