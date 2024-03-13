from queue import PriorityQueue
from typing import Dict, List, Tuple
import cv2
import numpy as np
import pickle
import math

def find_closest(point: Tuple[int, int], roads: Dict[Tuple, List]) -> Tuple[int, int]:
    x0, y0 = point
    dt = None
    closest_point = None
    for x, y in roads:
        d = math.sqrt((x0-x)*(x0-x) + (y0-y)*(y0-y))
        dt, closest_point = (d, (x, y)) if (dt is None and closest_point is None) or d < dt else (dt, closest_point)

    return closest_point
        
def get_roads(filename: str) -> Dict[Tuple, List]:
    with open(filename, 'rb') as f:
        return pickle.load(f)

def scaled_point(
    map_shape: Tuple[int, int, int],
    map_info: Tuple[int, int, int, int],
    P: Tuple[int, int]
) -> Tuple[int, int]:
    min_x, max_x, min_y, max_y = map_info
    wd = max_x - min_x
    ht = max_y - min_y

    x, y = P

    return int((x - min_x) / wd * map_shape[1]), int((max_y - y) / ht * map_shape[0])


def draw_line(
    ar_map: np.ndarray, 
    map_info: Tuple[int, int, int, int],
    p0: Tuple[int, int],
    p1: Tuple[int, int], 
    color: Tuple[int, int, int] = (0,0,0),
    thickness: int = 1
) -> None:

    min_x, max_x, min_y, max_y = map_info
    wd = max_x - min_x
    ht = max_y - min_y

    s_f = scaled_point(ar_map.shape, map_info, p0)
    s_t = scaled_point(ar_map.shape, map_info, p1)
    '''
    x_f, y_f = p0
    sx_f, sy_f = (x_f - min_x) / wd * ar_map.shape[1], (max_y - y_f) / ht * ar_map.shape[0]
    sx_f, sy_f = int(sx_f), int(sy_f)

    x_t, y_t = p1
    sx_t, sy_t = (x_t - min_x) / wd * ar_map.shape[1], (max_y - y_t) / ht *ar_map.shape[0]
    sx_t, sy_t = int(sx_t), int(sy_t)
    '''

    cv2.line(ar_map, s_f, s_t, color, thickness=thickness)

def get_distance(p0: Tuple[int, int], p1: Tuple[int, int]) -> float:
    lon0, lat0 = p0
    lon1, lat1 = p1

    lon0, lat0 = lon0 / 100_000, lat0 / 100_000
    lon1, lat1 = lon1 / 100_000, lat1 / 100_000

    R = 3958.8 # mi
    P = math.pi / 180

    a = 0.5 - math.cos((lat1-lat0)*P)/2 + math.cos(lat0*P) * math.cos(lat1*P) * (1-math.cos((lon1-lon0)*P))/2
    return 2 * R * math.asin(math.sqrt(a))

def create_map(roads: Dict[Tuple, List], show: bool = False):
    max_x = None
    min_x = None
    max_y = None
    min_y = None
    for x, y in roads:
        max_x = x if max_x is None else max(max_x, x)
        min_x = x if min_x is None else min(min_x, x)
        max_y = y if max_y is None else max(max_y, y)
        min_y = y if min_y is None else min(min_y, y)

    map_info = (min_x, max_x, min_y, max_y)

    map_shape = (int(1080*2), int(1080*2))

    ar_map = np.ones((map_shape[1], map_shape[0], 3), dtype=np.uint8)*255

    for frame, f in enumerate(roads):
        for t in roads[f]:

            draw_line(ar_map, map_info, f, t)

            if show and frame % 1000 == 0:
                cv2.imshow('map', ar_map)
                if cv2.waitKey(1) == ord('q'):
                    exit()

    return ar_map, map_info

def heuristic(P: Tuple[int, int], G: Tuple[int, int]):
    return get_distance(P, G)

def dijkstra(
    ar_map: np.ndarray,
    map_info: Tuple[int, int, int, int],
    root: Tuple[int, int],
    goal: Tuple[int, int],
    roads: Dict[Tuple, List],
    video: cv2.VideoWriter,
    show: bool = False,
    astar: bool = False,
    zoom: float = 1
) -> List[Tuple[int, int]]:

    zp = ((root[0] + goal[0])/2, (root[1] + goal[1])/2)
    zp = scaled_point(ar_map.shape, map_info, zp)


    parents = {}

    pq = PriorityQueue()
    visited = set([root])
    pq.put((0, *root))

    frame = 0
    while pq.queue:
        N = pq.get_nowait()

        c, x, y = N
        P = (x, y)
        if P == goal:
            break

        for edge in roads[P]:
            if edge in visited:
                continue

            draw_line(ar_map, map_info, P, edge, color=(255, 0, 0), thickness=2)


            ce = c + get_distance(P, edge) * 0.9 + heuristic(edge, goal) * 0.1 if astar else c + get_distance(P, edge)
            pq.put((ce, *edge))
            visited.add(edge)
            parents[edge] = P

        if show and frame % 50 == 0:
            zmap = zoom_at(ar_map[::], zoom, zp)
            video.write(cv2.resize(zoom_at(ar_map[::], zoom, zp), (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
            cv2.imshow('map', zmap)
            if cv2.waitKey(1) == ord('q'):
                exit()
        frame += 1

    path = [goal]
    N = goal
    while (N := parents[N]) != root:
        path.append(N)
    path.append(root)

    return path[::-1]

def trace_forward(
    ar_map: np.ndarray,
    map_info: Tuple[int, int, int, int],
    path: List[Tuple[int, int]],
    video: cv2.VideoWriter,
    zoom: float = 1,
) -> None:
    tot_d = 0
    for i in range(len(path)-1):
        f, t = path[i], path[i+1]
        tot_d += get_distance(path[i], path[i+1])

        draw_line(ar_map, map_info, f, t, color=(0, 0, 255), thickness=2)

        if i % 2 == 0:
            zx, zy = (path[0][0] + path[-1][0])/2, (path[0][1] + path[-1][1])/2
            zp = scaled_point(ar_map.shape, map_info, (zx, zy))

            video.write(cv2.resize(zoom_at(ar_map[::], zoom, zp), (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
            cv2.imshow('map', zoom_at(ar_map[::], zoom, zp))
            if cv2.waitKey(1) == ord('q'):
                exit()
    print(tot_d)

def zoom_at(img, zoom, coord=None):
    if zoom == 1:
        return img
    # Translate to zoomed coordinates
    h, w, _ = [ zoom * i for i in img.shape ]
    
    if coord is None: cx, cy = w/2, h/2
    else: cx, cy = [ zoom*c for c in coord ]
    
    img = cv2.resize( img, (0, 0), fx=zoom, fy=zoom, interpolation=cv2.INTER_NEAREST)
    img = img[ int(round(cy - h/zoom * .5)) : int(round(cy + h/zoom * .5)),
               int(round(cx - w/zoom * .5)) : int(round(cx + w/zoom * .5)),
               : ]
    
    return img

if __name__ == '__main__':


    roads = get_roads('roads_processed.pickle')
    ar_map, map_info = create_map(roads, show=False)

    scale = 1
    dim = (scale*ar_map.shape[1], scale*ar_map.shape[0])
    video = cv2.VideoWriter('t.mp4', cv2.VideoWriter_fourcc(*'avc1'), 30, dim)

    asmsa = find_closest((-9306061, 3451811), roads)
    home = find_closest((-9241347, 3469794), roads)

    zx, zy = (asmsa[0] + home[0])/2, (asmsa[1] + home[1])/2
    zp = scaled_point(ar_map.shape, map_info, (zx, zy))
    zoom = 1

    for _ in range(int(30*3.5)):
        video.write(cv2.resize(zoom_at(ar_map[::], zoom, zp), (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        cv2.imshow('map', zoom_at(ar_map[::], zoom, zp))
        cv2.waitKey(1)

    path = dijkstra(ar_map, map_info, asmsa, home, roads, video, show=True, astar=True, zoom=zoom)

    for _ in range(int(30*3.5)):
        video.write(cv2.resize(zoom_at(ar_map[::], zoom, zp), (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        cv2.imshow('map', zoom_at(ar_map[::], zoom, zp))
        cv2.waitKey(1)

    trace_forward(ar_map, map_info, path, video, zoom=zoom)

    for _ in range(int(30*3.5)):
        video.write(cv2.resize(zoom_at(ar_map[::], zoom, zp), (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST))
        cv2.imshow('map', zoom_at(ar_map[::], zoom, zp))
        cv2.waitKey(1)

    video.release()


