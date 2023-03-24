import csv
import sklearn
from sklearn.neural_network import MLPClassifier
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler

data = list(csv.reader(open('triangles.csv')))
X = []
y = []
for a, b, c, t in data:
    X.append(sorted([int(a), int(b), int(c)]))
    y.append(t)

X, y = shuffle(X,y)
scalar = StandardScaler()
scalar.fit(X)
X=scalar.transform(X)

clf = MLPClassifier(hidden_layer_sizes=[100,100,100], max_iter=10000000)
clf.fit(X,y)
import numpy as np
import cv2
img = np.zeros((200,200),dtype=np.uint8)
actual = np.zeros((200,200),dtype=np.uint8)

for a in range(200):
    for b in range(200):
        c=100;
        tritype=clf.predict(scalar.transform([sorted([a,b,c])]))[0]
        if tritype=="acute":
            img[a,b]=128
        if tritype=="obtuse":
            img[a,b]=255

        i,j,k = sorted([a,b,c])
        if i+j>k and i*i+j*j<k*k:
            actual[a,b]=255
        if i+j>k and i*i+j*j>k*k:
            actual[a,b]=128
