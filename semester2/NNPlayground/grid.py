import csv
from sklearn.model_selection import GridSearchCV
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
scalar: StandardScaler = StandardScaler()
scalar.fit(X)

X=scalar.transform(X)
print(type(X))

clf = MLPClassifier(hidden_layer_sizes=[100,100,100], max_iter=10000)
parameters = {'hidden_layer_sizes':[[10],[20]],
              'activation':['identity', 'logistic', 'tanh', 'relu'],
              'solver':['lbfgs', 'sgd', 'adam']}
grid = GridSearchCV(clf, parameters, cv=3, n_jobs=6, verbose=100)
grid.fit(X,y);
