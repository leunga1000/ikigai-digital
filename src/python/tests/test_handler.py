import json
import pytest
from handler import lambda_handler, balances
from collections import defaultdict

def test():
    assert 1==1

def test_transaction():
    account1 = 123
    account2 = 456
    amount = 100
    balances[account1] = 1000
    balances[account2] = 1000
    event = {"body":
              {"accountFrom": account1, 
               "accountTo": account2,
               "amount": amount,
               "transactionType": "DEBIT"}
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 200
    body = json.loads(data['body'])
    assert body['previousBalance'] == 1000.00
    assert body['currentBalance'] == 900.00

def test_transaction():
    account1 = 123
    account2 = 456
    amount = 100
    balances[account1] = 1000
    balances[account2] = 1000
    event = {"body":
              {"accountFrom": account1, 
               "accountTo": account2,
               "amount": amount,
               "transactionType": "CREDIT"}
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 200
    body = json.loads(data['body'])
    assert body['previousBalance'] == 1000.00
    assert body['currentBalance'] == 1100.00


def test_incomplete_input():
    account1 = 123
    account2 = 456
    amount = 100
    balances[account1] = 0  # {account1: 1000, account2: 1000}
    balances[account2] = 0

    event = {"body":
              {#"accountFrom": account1, 
               "accountTo": account2,
               "amount": amount,
               "transactionType": "DEBIT"}
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INTERNAL_SERVER_ERROR"

    event = {"body":
              {"accountFrom": account1, 
               # "accountTo": account2,
               "amount": amount,
               "transactionType": "DEBIT"}
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INTERNAL_SERVER_ERROR"
    # assert body['errorMessage'] == f"Insufficient Balance in {account1}"

    event = {"body":
              {"accountFrom": account1, 
               "accountTo": account2,
               #"amount": amount,
               "transactionType": "DEBIT"}
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INTERNAL_SERVER_ERROR"
    # assert body['errorMessage'] == f"Insufficient Balance in {account1}"


    event = {"body":
              {"accountFrom": account1, 
               "accountTo": account2,
               "amount": amount,
               # "transactionType": "DEBIT"
               }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INTERNAL_SERVER_ERROR"
    # assert body['errorMessage'] == f"Insufficient Balance in {account1}"

def test_wrong_input():
    account1 = 123
    account2 = 456
    amount = 100
    balances[account1] = 0  # {account1: 1000, account2: 1000}
    balances[account2] = 0

    event = {"body":
              {"accountFrom": "asdf", 
               "accountTo": account2,
               "amount": amount,
               "transactionType": "DEBIT"}
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INTERNAL_SERVER_ERROR"

    event = {"body":
              {"accountFrom": account1, 
               "accountTo": "asdf",
               "amount": amount,
               "transactionType": "DEBIT"}
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INTERNAL_SERVER_ERROR"
    # assert body['errorMessage'] == f"Insufficient Balance in {account1}"

    event = {"body":
              {"accountFrom": account1, 
               "accountTo": account2,
               "amount": "asdf",
               "transactionType": "DEBIT"}
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INTERNAL_SERVER_ERROR"
    # assert body['errorMessage'] == f"Insufficient Balance in {account1}"


    event = {"body":
              {"accountFrom": account1, 
               "accountTo": account2,
               "amount": amount,
               "transactionType": "NONSENSE"
               }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INTERNAL_SERVER_ERROR"



def test_no_body():
    event = {"bodywrong":
              {#"accountFrom": account1, 
               #"accountTo": account2,
               
               "amount": 0
               # "transactionType": "DEBIT"
               }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INTERNAL_SERVER_ERROR"
            

def test_insufficient_balance():
    account1 = 123
    account2 = 456
    amount = 100
    balances[account1] = 0 # {account1: 1000, account2: 1000}
    balances[account2] = 0
    event = {"body":
              {"accountFrom": account1, 
               "accountTo": account2,
               "amount": amount,
               "transactionType": "DEBIT"}
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INSUFFICIENT_BALANCE"
    assert body['errorMessage'] == f"Insufficient Balance in {account1}"

def test_insufficient_balance_with_str_body():
    account1 = 123
    account2 = 456
    amount = 100
    balances[account1] = 0 # {account1: 1000, account2: 1000}
    balances[account2] = 0
    event = {"body":
              json.dumps({"accountFrom": account1, 
               "accountTo": account2,
               "amount": amount,
               "transactionType": "DEBIT"}
              )}
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INSUFFICIENT_BALANCE"
    assert body['errorMessage'] == f"Insufficient Balance in {account1}"
