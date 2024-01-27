import numpy as np
import cv2
import time
from functools import partial
import multiprocessing as mp

def makePretty(A):
    O = np.zeros((512,512,3), dtype=np.uint8)
    O[A==0] = (255,200,200)
    O[A==1] = (40,60,100)
    return O

def loadCave(filename):
    cave_bytes=np.fromfile(filename, dtype=np.uint8)
    cave_bits=np.unpackbits(cave_bytes)
    cave=np.reshape(cave_bits,(512,512,512))
    return cave

def saveCave(cave,filename):
	np.packbits(np.uint8(np.ravel(cave))).tofile(filename)

def side_change(A, val):
    cv2.imshow("side view", makePretty(A[:,val,:]))

def top_change(A, val):
    cv2.imshow("top view", makePretty(A[val,:,:]))


def get_cost(A, C):
    z, y, x = C
    '''
    B_VOL = np.count_nonzero(A[z-20:z+21,y-20:y+21,x-20:x+21])
    T = (1-A[z-25:z+26,y-25:y+26,x-25:x+26])
    W_EMP = np.count_nonzero(T) - np.count_nonzero(T[5:46,5:46,5:46])
    '''

    B_VOL = A[z-20:z+21,y-20:y+21,x-20:x+21].sum() # amount of dirt in burrow
    T = (1-A[z-25:z+26,y-25:y+26,x-25:x+26]) # amount of air in the burrow + wall
    W_EMP = T.sum() - (T[5:46,5:46,5:46]).sum() # amount of air in the wall

    return (B_VOL >= W_EMP, 2*B_VOL, C, int(B_VOL)-int(W_EMP))
    
def find_spots(A):
    # Idea:
    # Look for where the dirt in burrow >= empty space in wall/shell
    # Then, to build burrows, just set burrow to 0,
    # replace all empty space in wall to 1,
    # then all extra dirt in the burrow is put outside
    K = [(z,y,x) for z, S in enumerate(A[25:512-26], 25) for y, R in enumerate(S[25:512-26], 26) for x, C in enumerate(R[25:512-25], 26) if not C]

    pool = mp.Pool(processes=24)
    t0 = time.time()

    N = [(cost, coord, leftover) for V, cost, coord, leftover in pool.map(partial(get_cost, A), K) if V and leftover >= 0]
    t = time.time()
    print(f'finished getting costs in: {int(t-t0)} seconds')

    N = sorted(N, key=lambda n: n[0])
    valids = [N[0]]
    for n in N[1:]:
        if len(valids) == 4:
            break

        _, ncoord, _ = n
        good = True
        for v in valids:
            _, vcoord, _ = v
            if ((vcoord[0]-25 <= ncoord[0]-25 <= vcoord[0]+25 or vcoord[0]-25 <= ncoord[0]+25 <= vcoord[0]+25) or
                (vcoord[1]-25 <= ncoord[1]-25 <= vcoord[1]+25 or vcoord[1]-25 <= ncoord[1]+25 <= vcoord[1]+25) or
                (vcoord[2]-25 <= ncoord[2]-25 <= vcoord[2]+25 or vcoord[2]-25 <= ncoord[2]+25 <= vcoord[2]+25)):
                good = False
                break
        if good:
            valids.append(n)

    for n in valids:
        print(n)

    caves = []
    for cost, coord, leftover in valids:
        C = make_burrow(A[::], coord, leftover)
        caves.append(C)
        saveCave(C, f'burrowcity_{coord[2]}_{coord[1]}_{coord[0]}_{int(cost)}_orlinab24.cave')

    '''
    for cave in caves:
        cv2.imshow("side view", makePretty(cave[:,0,:]))
        cv2.createTrackbar('slider', "side view", 0, 511, partial(side_change, cave))
        cv2.imshow("top view", makePretty(cave[0,:,:]))
        cv2.createTrackbar('slider', "top view", 0, 511, partial(top_change, cave))
        cv2.waitKey(0)
    '''

def make_burrow(A, coord, leftover):
    z, y, x = coord
    L = leftover
    A[z-25:z+26,y-25:y+26,x-25:x+26] = 1
    A[z-20:z+21,y-20:y+21,x-20:x+21] = 0

    for x in range(x-25,x+26):
        for y in range(y-25,y+26):
            for z in range(z+26,z+26+L):
                if z >= 512:
                    break
                if A[z,y,x]:
                    break
                if not leftover:
                    break

                A[z,y,x] = 1
                leftover -= 1

            if not leftover:
                break
        if not leftover:
            break

    return A

if __name__ == '__main__':
    inp=loadCave('./input.cave')

    find_spots(inp)

