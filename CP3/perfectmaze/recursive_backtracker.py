from collections import deque
from random import choice
import numpy as np
import cv2

local_to_map = lambda N: (4*N[0]+2, 4*N[1]+2)

dim = 30
scale = 10
v_fps = 90
res = ((4*dim+1)*scale, (4*dim+1)*scale)
video = cv2.VideoWriter('recursive_backtracker.mp4', cv2.VideoWriter_fourcc(*'avc1'), v_fps, res)

def get_neighbours(P):
    y, x = P
    return (y-1, x), (y, x+1), (y+1, x), (y, x-1)

def recursive_backtracker(dim: int, show: bool=False):
    Q = deque([(0,0)])
    adjacents = {(0,0):[]}

    map = np.full((4*dim+1, 4*dim+1, 3), (90,71,69), dtype=np.uint8)
    map[::4,::] = (68,50,49)
    map[::,::4] = (68,50,49)

    valid_node = lambda N: 0<=N[0]<=dim-1 and 0<=N[1]<=dim-1 and N not in adjacents

    while Q:
        N = Q[-1]
        neighbours = list(filter(valid_node, get_neighbours(N)))

        if neighbours:
            neighbour = choice(neighbours)
            Q.append(neighbour)

            nbr_adjacents = adjacents.get(neighbour, [])
            nbr_adjacents.append(N)
            adjacents[neighbour] = nbr_adjacents

            N_adjacents = adjacents.get(N, [])
            N_adjacents.append(neighbour)
            adjacents[N] = N_adjacents

            N_y, N_x = local_to_map(N)
            nbr_y, nbr_x = local_to_map(neighbour)
            wall_y, wall_x = (N_y+nbr_y) // 2, (N_x+nbr_x) // 2
            
            if wall_y == N_y:
                f, t = min(N_x, nbr_x), max(N_x, nbr_x)
                map[wall_y-1:wall_y+2, f-1:t+2] = (172, 160, 235)
            elif wall_x == N_x:
                f, t = min(N_y, nbr_y), max(N_y, nbr_y)
                map[f-1:t+2, wall_x-1:wall_x+2] = (172, 160, 235)
        else:
            N_y, N_x = local_to_map(N)
            for neighbour in adjacents.get(N, []):
                nbr_y, nbr_x = local_to_map(neighbour)
                f_y, f_x = min(N_y, nbr_y), min(N_x, nbr_x)
                t_y, t_x = max(N_y, nbr_y), max(N_x, nbr_x)
                map[f_y-1:t_y+2, f_x-1:t_x+2] = (254, 190, 180)
            Q.pop()

        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        if show:
            cv2.imshow("map", cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
            cv2.waitKey(5)

    return adjacents, map

def solver(adjacents, map):

    root = (0,0)
    end_node = (dim-1, dim-1)
    Q = deque([root])
    visited = set([root])

    parents = {}

    found = False

    while Q:
        N = Q.popleft()

        for edge in adjacents[N]:
            if edge in visited:
                continue

            Q.append(edge)
            visited.add(edge)
            parents[edge] = N
            
            N_y, N_x = local_to_map(N)
            e_y, e_x = local_to_map(edge)
            f_y, f_x = min(N_y, e_y), min(N_x, e_x)
            t_y, t_x = max(N_y, e_y), max(N_x, e_x)
            map[f_y-1:t_y+2, f_x-1:t_x+2] = (220, 224, 245)
            video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))

            if edge == end_node:
                found = True
                break
            '''
            cv2.imshow("map", cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
            cv2.waitKey(50)
            '''

        if found:
            break

    path = [end_node]
    N = end_node
    while (N := parents[N]) != root:
        path.append(N)
    path.append(root)

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

    adjacents, map = recursive_backtracker(dim, show=False)
    for _ in range(v_fps*2):
        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))

    solve_path = solver(adjacents, map)
    for _ in range(v_fps*2):
        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))

    walk_path(solve_path, map)
    for _ in range(v_fps*2):
        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))

    video.release()

    '''
    cv2.imshow("map", cv2.resize(map, (0,0), fx=10, fy=10, interpolation=cv2.INTER_NEAREST))
    cv2.waitKey(0)
    '''

