import numpy as np
import cv2

def make_img(top, A, file):
    O = np.zeros((512,512,3), dtype=np.uint8)
    O[A[top]==0] = (255,200,200)
    O[A[top]==1] = (40,60,100)
    cv2.imwrite(file, O)

def loadCave(filename):
    cave_bytes=np.fromfile(filename, dtype=np.uint8)
    cave_bits=np.unpackbits(cave_bytes)
    cave=np.reshape(cave_bits,(512,512,512))
    return cave

if __name__ == '__main__':
    C0 = loadCave('./burrowcity_460_275_239_39446_orlinab24.cave')
    make_img(239, C0, 'burrowcity_460_275_239_39446_orlinab24.png')

    C1 = loadCave('./burrowcity_163_476_440_40236_orlinab24.cave')
    make_img(440, C1, 'burrowcity_163_476_440_40236_orlinab24.png')

    C2 = loadCave('./burrowcity_247_32_365_40370_orlinab24.cave')
    make_img(365, C2, 'burrowcity_247_32_365_40370_orlinab24.png')

    C3 = loadCave('./burrowcity_323_132_117_43244_orlinab24.cave')
    make_img(117, C3, 'burrowcity_323_132_117_43244_orlinab24.png')
