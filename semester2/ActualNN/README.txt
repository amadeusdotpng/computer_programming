protoNN.py does:
- preprocesses the data files from ./data
- tokenizes the data using sklearn's TfidVectorizer
- trains the MLP
- prints out its fitness score
- saves the model to 'model.pkl' using python's pickle

you can use 'predict.py' to test out the model with other files.
you must run 'python protoNN.py' first to create a model to use 'predict.py'

