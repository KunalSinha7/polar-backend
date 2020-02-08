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

```
nose2 -v
```

To make new test cases the filename must start with ```test_``` and methodnames must start with ```test_```.