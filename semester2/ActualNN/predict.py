import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier

with open('data/keywords.txt', 'r') as f:
    keywords = np.array([line.strip() for line in f.readlines()])

vectorizer = TfidfVectorizer(lowercase=False)
vectorizer.fit(keywords)

with open('model.pkl', 'rb') as f:
    clf = pickle.load(f)

directory = input('provide a valid path to a file you want to test\n')

with open(directory, 'r') as f:
    data = [' '.join([line.strip() for line in f.readlines()])]
    vector = vectorizer.transform(data)
    print(f'This file is: {clf.predict(vector.toarray())[0]}\n')
