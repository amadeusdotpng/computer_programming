# Usage
Create a model first. This will output `model.pkl`.
```cmd
python protoNN.py
```

Test using your own data  
```cmd
# Test directory structure should be like:  
# path_to_test
# ├── cpp
# │  ├── file1.cpp
# │  └── ...
# ├── java
# │  ├── file1.java
# │  └── ...
# ├── python
# │  ├── file1.py
# │  └── ...
# └── rust
#    ├── file1.rs
#    └── ...

python test.py path_to_test
```

Use `model.pkl` to predict file language
```cmd
# For single files
python predict.py path/to/file

# For entire directory
python predict.py -d path/to/directory
```

Produce confusion matrix
```cmd
python confusion.py
```
