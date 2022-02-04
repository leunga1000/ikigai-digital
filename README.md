# ikigai-digital

## Running:
### To build and run the docker container, in the directory with the Makefile

```sh
make docker-run
```

### Then send events to your Docker instance at localhost:80

```sh
curl -XPOST "http://localhost/2015-03-31/functions/function/invocations" -d "{your_data_here}"
```


### Alternatively use call_lambda.py to circumvent shell escaping issues - see the setup tests in the Testing section below to install requests library

```sh
python call_lambda.py
```

## Testing:

### Install the pytest and coverage packages in your virtual environment created in the manner of your choice, e.g. 

```sh
pip install virtualenvwrapper
mkvirtualenv idtest
pip install -r requirements.txt
```

### To run pytest, in the directory with the Makefile:

```sh
make test
```

### To display coverage:

```sh
make coverage
```


## Assumptions:
### Task is to implement a lambda that takes in transactions and call a 3rd party API and return the result to the mobile app.

### Authentication and Authorization, API keys
Would need to be part of a production application.

### 3rd party API
Some questions from the 3rd party API - amount is specified as int, with format double.
Transaction returns balance - but of which account.
