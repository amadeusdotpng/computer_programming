import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.utils import shuffle

with open('keywords.txt', 'r') as f:
    keywords = np.array([line.strip() for line in f.readlines()])

vectorizer = TfidfVectorizer(lowercase=False)
vectorizer.fit(keywords)

X = []
y = []

def add_files(dataList, targetList, dir, target):
    for i, file in enumerate(os.listdir(dir)):
        if i >= 500:
            break
        
        file = open(os.path.join(dir, file))
        data = [' '.join([line.strip() for line in file.readlines()])]
        vector = vectorizer.transform(data)
        dataList.append(vector.toarray()[0])
        targetList.append(target)


add_files(X, y, './data/java'  , 'java')
add_files(X, y, './data/cpp'   , 'cpp')
add_files(X, y, './data/python', 'python')
add_files(X, y, './data/rust'  , 'rust')

X, y = shuffle(X, y)
print(np.array(X).shape)
clf = MLPClassifier(hidden_layer_sizes=[1000,1000,1000], max_iter=10000000, verbose=True)
# clf = MLPClassifier(max_iter=10000000, verbose=True)
clf.fit(X[:400*4], y[:400*4])
print(clf.score(X[400*4:], y[400*4:]))

with open('model.pkl', 'wb') as f:
    pickle.dump(clf, f)

    
