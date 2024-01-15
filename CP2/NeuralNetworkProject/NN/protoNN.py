import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
from pprint import pprint

with open('keywords.txt', 'r') as f:
    keywords = np.array([line.strip() for line in f.readlines()])

vectorizer = TfidfVectorizer(lowercase=False)
vectorizer.fit(keywords)

def add_files(dir, target):
    data_list = []
    target_list = []
    for i, file in enumerate(os.listdir(dir)):
        if i >= 500:
            break

        file = open(os.path.join(dir, file))
        data_list.append(' '.join([line.strip() for line in file.readlines()]))
        target_list.append(target)

    data_list = vectorizer.transform(data_list).toarray()
    return list(data_list), target_list

java_X,   java_y   = add_files('./data/java'  , 'java')
cpp_X,    cpp_y    = add_files('./data/cpp'   , 'cpp')
python_X, python_y = add_files('./data/python', 'python')
rust_X,   rust_y   = add_files('./data/rust'  , 'rust')

X = java_X + cpp_X + python_X + rust_X
y = java_y + cpp_y + python_y + rust_y

X, y = shuffle(X, y)
# GridSearchCV stuff to find the best parameters
'''
params = {'hidden_layer_sizes':[[100, 100, 100]],
          'activation': ['identity', 'logistic', 'tanh', 'relu'],
          'solver': ['lbfgs', 'sgd', 'adam']}
mlp = MLPClassifier(max_iter=100000000, verbose=False)

clf = GridSearchCV(mlp, params)
clf.fit(X[:400*4], y[:400*4])

table = pd.DataFrame(data=clf.cv_results_)
table.to_csv('gridsearch_results.csv')
print(f'best parameters found: {clf.best_params_}')
print(clf.score(X[400*4:], y[400*4:]))
'''

'''
params = {'hidden_layer_sizes':[[2],[10],[100],
                               [2,2],[10,10],[100,100],
                               [2,2,2],[10,10,10],[100,100,100]]}

mlp = MLPClassifier(max_iter=100000000,
                    activation = 'tanh',
                    solver = 'adam',
                    verbose=False)

clf = GridSearchCV(mlp, params)
clf.fit(X[:400*4], y[:400*4])

table = pd.DataFrame(data=clf.cv_results_)
table.to_csv('neuronsearch_results.csv')
print(f'best parameters found: {clf.best_params_}')
print(clf.score(X[400*4:], y[400*4:]))
'''

# Number of Data
for N in range(1, 400):
    clf = MLPClassifier(hidden_layer_sizes = [10],
                        activation = 'tanh',
                        solver = 'adam',
                        max_iter = 100000000,
                        random_state = 12345,
                        verbose = False)

    clf.fit(X[:N*4], y[:N*4])

    # Test Model
    print(f'{N},{clf.score(X[400:], y[400:])}')

# Save Model
with open('model.pkl', 'wb') as f:
    pickle.dump(clf, f)

    
