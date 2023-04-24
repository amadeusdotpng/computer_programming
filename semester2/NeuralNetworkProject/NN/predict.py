import pickle
import numpy as np
import argparse
import os
from sklearn.feature_extraction.text import TfidfVectorizer

def main(path, is_directory):
    with open('keywords.txt', 'r') as f:
        keywords = np.array([line.strip() for line in f.readlines()])

    vectorizer = TfidfVectorizer(lowercase=False)
    vectorizer.fit(keywords)

    with open('model.pkl', 'rb') as f:
        clf = pickle.load(f)

    if not is_directory:
        data = [preprocess_file(path)]

        pred = predict(data, clf, vectorizer)[0]
        name = '/'.join(path.split('/')[-2:])
        print(f'{name} is {pred}')
    else:
        dirs = [os.path.join(path, file)for file in os.listdir(path)]
        data = [preprocess_file(file) for file in dirs]

        preds = predict(data, clf, vectorizer)
        for i, pred in enumerate(preds):
            name = '/'.join(dirs[i].split('/')[-2:])
            print(f'{name} is {pred}')



def preprocess_file(file_path):
    with open(file_path, 'r') as f:
        return ' '.join([line.strip() for line in f.readlines()])

def predict(data, clf, vectorizer):
    vector = vectorizer.transform(data)
    return clf.predict(vector.toarray())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE',
                        help = 'file to test')
    parser.add_argument('-d', dest='IS_DIRECTORY', action='store_true',
                        help='test on a whole directory instead of a single file')
    args = parser.parse_args()
    main(args.FILE, args.IS_DIRECTORY)
