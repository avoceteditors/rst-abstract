
all: install builder

install:
	python3 setup.py install --user

builder: 
	sphinx-build -b meta example output

