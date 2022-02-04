# ikigai-digital

## Running:
To build and run the docker container:
```sh
make docker-run
```

Then send events to your Docker instance at localhost:80
```sh
curl -XPOST "http://localhost/2015-03-31/functions/function/invocations" -d "{}"
```

```sh
curl -XPOST "http://localhost/2015-03-31/functions/function/invocations" -d "{""body"": ""{""amount"": 30, ""accountFrom"": 123, ""accountTo"": 456, ""transactionType"": ""DEBIT""}""
```


## Testing:
Install the pytest and coverage packages in your virtual environment created in the manner of your choice, e.g. 
```sh
pip install virtualenvwrapper
mkvirtualenv idtest
```

```sh
pip install -r requirements.txt
```

To run pytest:
```sh
make test
```

To display coverage:
```sh
make coverage
```


## Assumptions:
Task is to implement a lambda that takes in transactions, updates a balance and returns the output of the transaction.

Presumably the balance would be held in a central location with atomicity and durability guarantees.

Some questions - amount is specified as int, with format double.
Transaction returns balance - but of which account, chose the From account.

