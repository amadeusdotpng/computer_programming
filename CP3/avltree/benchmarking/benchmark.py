from math import log
from random import seed
from typing import Tuple, Dict
from time import time_ns

from avltree import AVLTree
from redblacktree import rbtree
from ubtree import UBTree

import matplotlib.pyplot as plt
import numpy as np

def plot_data(data):
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    plt.figure(figsize=(1920*px, 1080*px))

    plt.title(data['title'])
    plt.xlabel(data['xlabel'])
    plt.ylabel(data['ylabel'])
    WW = 20
    for tree in data['trees']:
        X, Y = zip(*data['trees'][tree]['data'].items())
        cumsum_vec = np.cumsum(np.insert(Y, 0, 0)) 
        Y_ma = (cumsum_vec[WW:] - cumsum_vec[:-WW]) / WW

        C = data['trees'][tree]['color']
        L = data['trees'][tree]['label']
        plt.plot(X, Y, '.', color=C, label=L)
        plt.plot(X, Y, '-', color=C+'CC')
        plt.plot(X[WW//2-1:-WW//2], Y_ma, '-', color=C+'AA', label=L+' Moving Average')

    # plt.xscale('log', base=2)
    # plt.yscale('log', base=2)
    plt.legend()

def benchmark(T: str, N: int) -> Tuple[int, float, float, int]:
    K = np.arange(N)
    np.random.shuffle(K)
    
    tree = None
    match T:
        case 'avltree': tree = AVLTree()
        case 'rbtree':  tree = rbtree()
        case 'ubtree':  tree = UBTree()
    
    t0 = time_ns()
    for k in K:
        tree[k] = None
    t1 = time_ns()
    add_time = (t1 - t0)/1_000_000

    D = tree.depth()
    np.random.shuffle(K)

    del_time = 0
    if T != 'ubtree':
        t0 = time_ns()
        for k in K:
            del tree[k]
        t1 = time_ns()
        del_time = (t1 - t0)/1_000_000

    # (add total time, per add time, del total time, per del time, depth)
    return (N, (add_time, add_time/N, del_time, del_time/N, D))

def fullbenchmark(T: str, N: int) -> Dict:
    step = 125
    K = list(range(step, N, step))

    data = [benchmark(T, k) for k in K]

    return {
        'add_total_time':     {n: d[0] for n, d in data},
        'add_operation_time': {n: d[1] for n, d in data},
        'del_total_time':     {n: d[2] for n, d in data},
        'del_operation_time': {n: d[3] for n, d in data},
        'depth':              {n: d[4] for n, d in data},
    }


if __name__ == '__main__':
    seed(0xdeadbeef)
    N = 50000
    print('benchmarking for avltree...')
    avltree_data = fullbenchmark('avltree', N+1)
    print('done benchmarking avltree...')

    print('benchmarking rbtree...')
    rbtree_data  = fullbenchmark('rbtree', N+1)
    print('done benchmarking rbtree...')

    print('benchmarking ubtree...')
    ubtree_data  = fullbenchmark('ubtree', N+1)
    print('done benchmarking ubtree...')

    addttime_data = {
        'title': 'Total Time to Insert N Elements to a Tree',
        'xlabel': 'Number of Elements in Tree',
        'ylabel': 'Time Taken (ms)',
        'trees': {
            'avltree': {
                'color': '#7D3AC1',
                'label': 'AVL Tree Implementation',
                'data': avltree_data['add_total_time']
            },
            'rbtree': {
                'color': '#DB4CB2',
                'label': 'Red-Black Tree',
                'data': rbtree_data['add_total_time']
            },
            'ubtree': {
                'color': '#EA7369',
                'label': 'Unbalanced Tree',
                'data': ubtree_data['add_total_time']
            },
        },
    }

    addotime_data = {
        'title': 'Average Time Per Insert When Inserting N Elements to a Tree',
        'xlabel': 'Number of Elements in Tree',
        'ylabel': 'Time Taken (ms)',
        'trees': {
            'avltree': {
                'color': '#7D3AC1',
                'label': 'AVL Tree Implementation',
                'data': avltree_data['add_operation_time']
            },
            'rbtree': {
                'color': '#DB4CB2',
                'label': 'Red-Black Tree',
                'data': rbtree_data['add_operation_time']
            },
            'ubtree': {
                'color': '#EA7369',
                'label': 'Unbalanced Tree',
                'data': ubtree_data['add_operation_time']
            },
        },
    }

    delttime_data = {
        'title': 'Total Time to Delete N Elements from a Tree with N Elements',
        'xlabel': 'Number of Elements in Tree',
        'ylabel': 'Time Taken (ms)',
        'trees': {
            'avltree': {
                'color': '#7D3AC1',
                'label': 'AVL Tree Implementation',
                'data': avltree_data['del_total_time']
            },
            'rbtree': {
                'color': '#DB4CB2',
                'label': 'Red-Black Tree',
                'data': rbtree_data['del_total_time']
            },
        },
    }

    delotime_data = {
        'title': 'Average Time Per Delete When Deleting N Elements from a Tree with N Elements',
        'xlabel': 'Number of Elements in Tree',
        'ylabel': 'Time Taken (ms)',
        'trees': {
            'avltree': {
                'color': '#7D3AC1',
                'label': 'AVL Tree Implementation',
                'data': avltree_data['del_operation_time']
            },
            'rbtree': {
                'color': '#DB4CB2',
                'label': 'Red-Black Tree',
                'data': rbtree_data['del_operation_time']
            },
        },
    }

    depth_data = {
        'title': 'Depth of a Tree with N elements',
        'xlabel': 'Number of Elements in Tree',
        'ylabel': 'Depth',
        'trees': {
            'avltree': {
                'color': '#7D3AC1',
                'label': 'AVL Tree Implementation',
                'data': avltree_data['depth']
            },
            'rbtree': {
                'color': '#DB4CB2',
                'label': 'Red-Black Tree',
                'data': rbtree_data['depth']
            },
            'ideal': {
                'color': '#EA7369',
                'label': 'Ideal Depth',
                'data':  {n: log(n, 2)+1 for n in range(250, N, 250)}

            },
        },
    }

    plot_data(addttime_data)
    plt.savefig('addttime_data.png', dpi=400)
    plt.close()
    plot_data(addotime_data)
    plt.savefig('addotime_data.png', dpi=400)
    plt.close()
    plot_data(delttime_data)
    plt.savefig('delttime_data.png', dpi=400)
    plt.close()
    plot_data(delotime_data)
    plt.savefig('delotime_data.png', dpi=400)
    plt.close()
    plot_data(depth_data)
    plt.savefig('adddepth_data.png', dpi=400)
    plt.close()
