from queue import PriorityQueue
import numpy as np
import cv2

def get_neighbors(N):
    _, y, x = N
    return [(y-1, x), (y, x+1), (y+1, x), (y, x-1)]

def get_cost(c):
    match tuple(c):
        case (0  ,255,255): return 0 # yellow
        case (255,255,255): return 15 # white
        case (0  ,0  ,0  ): return 300 # black
        case (0  ,255,0  ): return 400 # green
        case (255,255,0  ): return 500 # cyan
        case (255,0  ,0  ): return 600 # blue
        case (0  ,0  ,255): return 100000 # red
        case _: raise Exception(c)

def dijkstra(root, map, video, scale, fps):
    overlay = np.full(map.shape, [255,0,255], dtype=np.uint8)
    color_map = cv2.addWeighted(map,0.9,overlay,0.5,0.5)
    root_with_cost = (get_cost(map[root]), *root)

    parents = {}
    pq = PriorityQueue()
    visited = set()
    pq.put(root_with_cost)

    end_node = None
    counter = 0

    while pq:
        counter = (counter + 1) % fps
        N = pq.get()

        c, y, x = N
        if tuple(map[y,x]) == (0, 255, 255):
            end_node = (y, x)
            break

        for edge in get_neighbors(N):
            ey, ex = edge

            if not (0 <= ey <= len(map)-1 and 0 <= ex <= len(map[ey])-1):
                continue

            if edge in visited:
                continue

            pq.put((c+get_cost(map[edge]), ey, ex))
            visited.add((ey, ex))
            parents[(ey,ex)] = (y, x)
            color_map[edge] = map[edge]

        if not counter:
            video.write(cv2.resize(color_map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
            cv2.imshow('color map', cv2.resize(color_map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
            cv2.waitKey(1)

    path = [end_node]
    N = end_node
    while (N := parents[N]) != root:
        path.append(N)
    path.append(root)

    return reversed(path)

if __name__ == '__main__':
    fps = 25
    map = cv2.imread('./map.png', cv2.IMREAD_COLOR)
    root = (2, 12)

    scale = 20
    dim = (scale*map.shape[1], scale*map.shape[0])
    video = cv2.VideoWriter('out.mp4', cv2.VideoWriter_fourcc(*'avc1'), fps, dim)

    for _ in range(int(fps*3.5)):
        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        cv2.imshow('color map', cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        cv2.waitKey(1)

    path = dijkstra(root, map, video, scale, fps)

    for y, x in path:
        map[y,x] = np.uint8((193, 182, 255))
        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        cv2.imshow('color map', cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        cv2.waitKey(1)

    for _ in range(int(fps*3.5)):
        video.write(cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        cv2.imshow('color map', cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        cv2.waitKey(1)

    video.release()

    cv2.imshow('color map', cv2.resize(map, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
    cv2.waitKey(1000)
