import numpy as np
import cv2

def makePretty(img):
    out=np.zeros((512,512,3),dtype=np.uint8)
    out[img==0]=(255,200,200)
    out[img==1]=(40,60,100)
    return out

def loadCave(filename):
    cave_bytes=np.fromfile(filename, dtype=np.uint8)
    cave_bits=np.unpackbits(cave_bytes)
    cave=np.reshape(cave_bits,(512,512,512))
    return cave

def saveCave(cave,filename):
	np.packbits(np.uint8(np.ravel(cave))).tofile(filename)


cave=loadCave("input.cave")
import time
start=time.time()
ogCave=cave*1
#Make a mock burrow.  I didn't conserve dirt.
print("dirt before",ogCave.sum())
print("air before",(1-ogCave).sum())
x,y,z=256,256,256
size=51
wall=5
buff=5
cave[x-size//2-wall:x+size//2+1+wall,
     y-size//2-wall:y+size//2+1+wall,
     z-size//2-wall:z+size//2+1+wall]=1
cave[x-size//2:x+size//2+1,y-size//2:y+size//2+1,z-size//2:z+size//2+1]=0
saveCave(cave,"output.cave")
print("cost",np.abs(cave*1.0-ogCave).sum() )
print("dirt after",cave.sum())
end=time.time()
print(end-start)


# ~ cv2.imshow("asdf",255-cave[:,:,5]*255)
# ~ cv2.waitKey(0)

#sliders can't hit every number
def side_change(val):
    cv2.imshow("side view", makePretty(cave[:,val,:]))
cv2.imshow("side view", makePretty(cave[:,0,:]))
cv2.createTrackbar('slider', "side view", 0, 511, side_change)
def top_change(val):
    cv2.imshow("top view", makePretty(cave[:,:,val]))
cv2.imshow("top view", makePretty(cave[:,:,0].T))
cv2.createTrackbar('slider', "top view", 0, 511, top_change)
cv2.waitKey(0)






