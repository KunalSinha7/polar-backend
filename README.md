# polar-backend


### How to run flask dev server. 

```
python3 flaskapp.py
```

or 

```
export FLASK_APP=flaskapp.py
export FLASK_ENV=development
flask run
```

The above allows lazy loading without rerunning the dev server.

### Running test cases

Run all
```
pytest -v
```

Running specific test cases
```
pytest -v test_file.py
pytest -v -k 'my classifier' i.e. (test_register)
```

To make new test cases the filename must start with ```test_```, class names must end with ```TestCase``` and method names must start with ```test_```.