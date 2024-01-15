import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_file(file_path):
    with open(file_path, 'r') as f:
        return ' '.join([line.strip() for line in f.readlines()])

def predict(data, clf, vectorizer):
    vector = vectorizer.transform(data)
    return clf.predict(vector.toarray())

with open('keywords.txt', 'r') as f:
    keywords = np.array([line.strip() for line in f.readlines()])

vectorizer = TfidfVectorizer(lowercase=False)
vectorizer.fit(keywords)

y_true = []
X = []

for lang in os.listdir('data'):
    path = os.path.join('data', lang)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        X.append(preprocess_file(file_path))
        y_true.append(lang)

with open('model.pkl', 'rb') as f:
    clf = pickle.load(f)

y_pred = predict(X, clf, vectorizer)

conf_matrix = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix,
                              display_labels=clf.classes_)
disp.plot()
plt.show()
