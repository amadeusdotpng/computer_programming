from collections import deque
from random import shuffle
from typing import Tuple
import numpy as np
import cv2

local_to_map = lambda N: (4*N[0]+2, 4*N[1]+2)

dim = 30
scale = 10
v_fps = 90
res = ((4*dim+1)*scale, (4*dim+1)*scale)
video = cv2.VideoWriter('kruskal.mp4', cv2.VideoWriter_fourcc(*'avc1'), v_fps, res)

class Node:
    def __init__(self, y: int, x: int):
        self.vertex = (y, x)
        self.adjacents = []
        self.parent = None

    def get_root(self):
        N = self
        while N.parent is not None:
            N = N.parent

        return N

    def union(self, other):
        other_root = other.get_root()
        other_root.parent = self
        self.adjacents.append(other)
        other.adjacents.append(self)

    def __str__(self):
        return f'{self.vertex}'

    def __repr__(self):
        return f'{self.vertex}'

def get_all_edges(dim: int):
    within_bounds = lambda N: 0<=N[0]<=dim-1 and 0<=N[1]<=dim-1

    for y in range(dim):
        for x in range(dim):
            yield from [
                ((y,x), E) 
                for E in filter(within_bounds, [(y-1, x),(y, x+1),(y+1, x),(y, x-1)])
            ]

def kruskal(dim: int):
    nodes = { 
        (y,x) : Node(y,x)
        for y in range(dim)
        for x in range(dim)
    }

    edges = deque(set(tuple(sorted(E)) for E in get_all_edges(dim)))
    shuffle(edges)

    map = np.full((4*dim+1, 4*dim+1, 3), (90,71, 69), dtype=np.uint8)
    map[::4,::] = (68,50,49)
    map[::,::4] = (68,50,49)


    while edges:
        N0, N1 = edges.pop()

        M0_y, M0_x = local_to_map(N0)
        M1_y, M1_x = local_to_map(N1)

        C0 = np.copy(map[M0_y,M0_x])
        C1 = np.copy(map[M1_y,M1_x])

        map[M0_y-1:M0_y+2,M0_x-1:M0_x+2] = (172, 160, 235)
        map[M1_y-1:M1_y+2,M1_x-1:M1_x+2] = (172, 160, 235)

        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        '''
        cv2.imshow("map", cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        cv2.waitKey(100)
        '''

        if nodes[N0].get_root() == nodes[N1].get_root():
            map[M0_y-1:M0_y+2,M0_x-1:M0_x+2] = C0
            map[M1_y-1:M1_y+2,M1_x-1:M1_x+2] = C1
            continue

        nodes[N0].union(nodes[N1])

        f_y, f_x = min(M0_y, M1_y), min(M0_x, M1_x)
        t_y, t_x = max(M0_y, M1_y), max(M0_x, M1_x)
        map[f_y-1:t_y+2, f_x-1:t_x+2] = (254, 190, 180)

        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        '''
        cv2.imshow("map", cv2.resize(map, (0,0), fx=10, fy=10, interpolation=cv2.INTER_NEAREST))
        cv2.waitKey(50)
        '''

    return nodes[(0,0)], map 

def solver(root: Node, map):
    end_vertex = (dim-1, dim-1)
    end_node = None
    Q = deque([root])
    visited = {root.vertex}

    parents = {}

    found = False
    while Q:
        N = Q.popleft()

        edges = N.adjacents

        for edge in edges:
            if edge is None:
                continue

            if edge.vertex in visited:
                continue

            Q.append(edge)
            visited.add(edge.vertex)

            parents[edge.vertex] = N.vertex

            N_y, N_x = local_to_map(N.vertex)
            e_y, e_x = local_to_map(edge.vertex)
            f_y, f_x = min(N_y, e_y), min(N_x, e_x)
            t_y, t_x = max(N_y, e_y), max(N_x, e_x)
            map[f_y-1:t_y+2, f_x-1:t_x+2] = (220, 224, 245)
            video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))

            if edge.vertex == end_vertex:
                end_node = edge
                found = True
                break

        if found:
            break


    path = [end_vertex]
    N = end_vertex
    while (N := parents[N]) != root.vertex:
        path.append(N)
    path.append(root.vertex)

    path = path[::-1]

    return path

def walk_path(solve_path, map):
    last_cell = solve_path[0]
    
    l_y, l_x = local_to_map(last_cell)

    map[l_y-1:l_y+2, l_x-1:l_y+2] = (231, 194, 245)
    video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))

    for cell in solve_path[1:]:
        l_y, l_x = local_to_map(last_cell)
        n_y, n_x = local_to_map(cell)
        f_y, f_x = min(l_y, n_y), min(l_x, n_x)
        t_y, t_x = max(l_y, n_y), max(l_x, n_x)

        map[f_y-1:t_y+2, f_x-1:t_x+2] = (231, 194, 245)
        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))

        last_cell = cell

if __name__ == '__main__':
    root, map = kruskal(dim)
    for _ in range(v_fps*2):
        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))

    solve_path = solver(root, map)
    for _ in range(v_fps*2):
        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))

    walk_path(solve_path, map)
    for _ in range(v_fps*2):
        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))

