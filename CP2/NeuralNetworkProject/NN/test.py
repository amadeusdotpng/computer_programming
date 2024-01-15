import pickle
import numpy as np
import argparse
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import shuffle

def main(test_directory):
    with open('keywords.txt', 'r') as f:
        keywords = np.array([line.strip() for line in f.readlines()])

    vectorizer = TfidfVectorizer(lowercase=False)
    vectorizer.fit(keywords)

    with open('model.pkl', 'rb') as f:
        clf = pickle.load(f)

    X, y = create_data(test_directory, vectorizer)
    print(clf.score(X, y))

def create_data(path, vectorizer):
    X = []
    y = []

    java_path   = os.path.join(path, 'java')
    cpp_path    = os.path.join(path, 'cpp')
    python_path = os.path.join(path, 'python')
    rust_path   = os.path.join(path, 'rust')

    java_X,   java_y   = process_directory(java_path, vectorizer, 'java')
    cpp_X,    cpp_y    = process_directory(cpp_path, vectorizer, 'cpp')
    python_X, python_y = process_directory(python_path, vectorizer, 'python')
    rust_X,   rust_y   = process_directory(rust_path, vectorizer, 'rust')

    X.extend(java_X)
    X.extend(cpp_X)
    X.extend(python_X)
    X.extend(rust_X)

    y.extend(java_y)
    y.extend(cpp_y)
    y.extend(python_y)
    y.extend(rust_y)

    X, y = shuffle(X, y)
    return X, y

def process_directory(path, vectorizer, target):
    X_unvectorized = []
    y = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        processed_file = ' '.join(line.strip() for line in open(file_path).readlines())
        X_unvectorized.append(processed_file)
        y.append(target)
    X = vectorizer.transform(X_unvectorized).toarray()
    return X, y

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('TEST_PATH',
                        help = 'path to test directory')
    args = parser.parse_args()
    main(args.TEST_PATH)
