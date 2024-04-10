from typing import Dict
from aohashtable import AOHashTable
from ihashtable import IHashTable
import time
from random import randrange

import matplotlib.pyplot as plt
import numpy as np

def draw(data: Dict, color: str, label: str, line: bool=False):
    plt.xticks(np.arange(0, 4201, 200))
    plt.xticks(rotation=40)
    plt.minorticks_on()
    plt.ylabel('Time (microseconds)')
    plt.xlabel('Number of Elements')
    if line:
        plt.plot(data.keys(), data.values(), '-o', label=label, markersize=2, linewidth=0.5, c='k', mec=color)
        plt.legend()
    else:
        plt.plot(data.keys(), data.values(), 'o', label=label, markersize=2, linewidth=0.5, c='k', mec=color)
        plt.legend()

def benchmark_per_operation(table: AOHashTable | IHashTable | Dict, n: int) -> Dict[int, float]:
    times = {}

    k = 30
    for i in range(0, n, k):
        t0 = time.time_ns()
        for j in range(k):
            table[str(i+j)] = i+j
        times[i] = (time.time_ns() - t0) / 1000

    return times

def benchmark_total_operation(table: AOHashTable | IHashTable | Dict, n: int) -> float:
    t0 = time.time_ns()
    for i in range(n):
        table[str(i)] = i
    return (time.time_ns()-t0) / 1000

def benchmark_avg_lookup(table: AOHashTable | IHashTable | Dict, n: int) -> float:
    for i in range(n):
        table[str(i)] = i
        # print(f'{table.key_table}\n{table.ckey_table} -> {n}\n')

    total_time = 0
    for _ in range(n):
        k = randrange(n)
        t0 = time.time_ns()
        try:
            table[str(k)]
        except:
            '''
            if type(table) == AOHashTable:
                print(f'AO: {table.key_table}')
            elif type(table) == IHashTable:
                print(f'I:  {table.key_table}\n{table.ckey_table}\n')
            '''
            raise Exception('i pooped my pants')
        total_time += time.time_ns() - t0

    return (total_time / 1000) / n

if __name__ == '__main__':
    step = 30
    benchmark_data = {
        'per_operation': {
            'AOHashTable': benchmark_per_operation(AOHashTable(), 4201),
            'IHashTable': benchmark_per_operation(IHashTable(), 4201),
            'Dict': benchmark_per_operation(dict(), 4201),
        },
        'total_operation': {
            'AOHashTable': dict((n, benchmark_total_operation(AOHashTable(), n)) for n in range(0, 4201, step)),
            'IHashTable': dict((n, benchmark_total_operation(IHashTable(), n)) for n in range(0, 4201, step)),
            'Dict': dict((n, benchmark_total_operation((dict()), n)) for n in range(0, 4201, step)),
        },
        'avg_lookup': {
            'AOHashTable': dict((n, benchmark_avg_lookup(AOHashTable(), n)) for n in range(step, 4201, step)),
            'IHashTable': dict((n, benchmark_avg_lookup(IHashTable(), n)) for n in range(step, 4201, step)),
            'Dict': dict((n, benchmark_avg_lookup(dict(), n)) for n in range(step, 4201, step)),
        }
    }

    draw(benchmark_data['total_operation']['AOHashTable'], color='red', label="All-at-Once Hash Table", line=True)
    draw(benchmark_data['total_operation']['IHashTable'], color='blue', label="Incremental Hash Table", line=True)
    draw(benchmark_data['total_operation']['Dict'], color='orange', label="Python Dictionary", line=True)
    plt.title('Time Taken To Add N Number of Elements To Hash Table')
    plt.show()

    draw(benchmark_data['per_operation']['AOHashTable'], 'red', label="All-at-Once Hash Table", line=True)
    draw(benchmark_data['per_operation']['IHashTable'], 'blue', label="Incremental Hash Table", line=True)
    draw(benchmark_data['per_operation']['Dict'], 'orange', label="Python Dictionary", line=True)
    plt.title('Time Taken Per 30 Elements To Reach 4200 Elements in Hash Table')
    plt.show()

    draw(benchmark_data['avg_lookup']['AOHashTable'], color='red', label="All-at-Once Hash Table")
    draw(benchmark_data['avg_lookup']['IHashTable'], color='blue', label="Incremental Hash Table")
    draw(benchmark_data['avg_lookup']['Dict'], color='orange', label="Python Dictionary")
    plt.title('Average Lookup Time in Hash Table with N Elements')
    plt.show()
