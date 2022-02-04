import json
import pytest
from handler import lambda_handler
from collections import defaultdict
import requests_mock

cb_url = 'http://corebanking-dev.com/transactions'

def test():
    assert 1==1


def test_transaction():

    account1 = "123"
    account2 = "456"
    amount = "100"
    event = {"body":
              {"account_from": account1, 
               "account_to": account2,
               "amount": amount,
               }
            }
    with requests_mock.Mocker() as m:
        m.post('http://corebanking-dev.com/transactions', json={'statusCode': 200, 'body': {'previousBalance': 1000, 'currentBalance': 900}})
        resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 200
    body = json.loads(data['body'])
    print(body)
    assert body['previousBalance'] == 1000.00
    assert body['currentBalance'] == 900.00


def test_incomplete_input():
    account1 = 123
    account2 = 456
    amount = 100
    
    event = {"body":
              {#"account_from": account1, 
               "account_to": account2,
               "amount": amount,
                }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "VALIDATION_ERROR"

    event = {"body":
              {"account_from": account1, 
               # "account_to": account2,
               "amount": amount,
                }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "VALIDATION_ERROR"
    # assert body['errorMessage'] == f"Insufficient Balance in {account1}"

    event = {"body":
              {"account_from": account1, 
               "account_to": account2,
               #"amount": amount,
               }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "VALIDATION_ERROR"
    # assert body['errorMessage'] == f"Insufficient Balance in {account1}"


def test_wrong_input():
    account1 = 123
    account2 = 456
    amount = 100

    event = {"body":
              {"account_from": "asdf", 
               "account_to": account2,
               "amount": amount,
               }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "VALIDATION_ERROR"

    event = {"body":
              {"account_from": account1, 
               "account_to": "asdf",
               "amount": amount,
               }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "VALIDATION_ERROR"
    # assert body['errorMessage'] == f"Insufficient Balance in {account1}"

    event = {"body":
              {"account_from": account1, 
               "account_to": account2,
               "amount": "asdf",
               }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "VALIDATION_ERROR"
    # assert body['errorMessage'] == f"Insufficient Balance in {account1}"


    event = {"body":
              {"account_from": account1, 
               "account_to": account2,
               "amount": -100,
               }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "VALIDATION_ERROR"



def test_no_body():
    event = {"bodywrong":
              {#"account_from": account1, 
               #"account_to": account2,
               
               "amount": 0
               # "transaction_type": "DEBIT"
               }
              }
    resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "VALIDATION_ERROR"
            

def test_insufficient_balance():
    account1 = 123
    account2 = 456
    amount = 100
    event = {"body":
              {"account_from": account1, 
               "account_to": account2,
               "amount": amount,
                }
              }
    with requests_mock.Mocker() as m:
        m.post(cb_url, status_code=500,
                       json={'statusCode': 500, 
                             'body':{'errorCode': 'INSUFFICIENT_BALANCE',
                                     'errorMessage': f'Insufficient Balance in {account1}'
                                    }
                            }
                )
        resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    print(body)
    assert body['errorCode'] == "INSUFFICIENT_BALANCE"
    assert body['errorMessage'] == f"Insufficient Balance in {account1}"


def test_insufficient_balance_with_str_body():
    account1 = 123
    account2 = 456
    amount = 100
    event = {"body":
              json.dumps({"account_from": account1, 
               "account_to": account2,
               "amount": amount,
               }
              )}
    with requests_mock.Mocker() as m:
        m.post(cb_url, status_code=500, 
               json={'statusCode': 500, 
                     'body': {'errorCode': 'INSUFFICIENT_BALANCE',
                              'errorMessage': f'Insufficient Balance in {account1}'
                              }
                    }
                )
        resp = lambda_handler(event, context=None)
    # data = json.loads(resp)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INSUFFICIENT_BALANCE"
    assert body['errorMessage'] == f"Insufficient Balance in {account1}"


def test_unknown_api_response_code():
    account1 = 123
    account2 = 456
    amount = 100
    event = {"body":
              json.dumps({"account_from": account1, 
               "account_to": account2,
               "amount": amount,
               }
              )}
    with requests_mock.Mocker() as m:
        m.post(cb_url, status_code=403, 
               json={'statusCode': 403, 
                     'body': {'errorCode': 'INTERNAL_SERVER_ERROR',
                              'errorMessage': f'Forbidden'
                              }
                    }
                )
        resp = lambda_handler(event, context=None)
    data = resp
    assert data['statusCode'] == 500
    body = json.loads(data['body'])
    assert body['errorCode'] == "INTERNAL_SERVER_ERROR"
    
