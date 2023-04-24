import csv
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

clf = MLPClassifier(hidden_layer_sizes=[100,100], max_iter=10000000000)
clf.fit(X[:5000],y[:5000])
print(clf.score(X[5000:],y[5000:]))
print(clf.score(X[:5000],y[:5000]))

