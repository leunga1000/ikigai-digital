import json
import logging
from decimal import Decimal
from collections import defaultdict

log = logging.getLogger()
log.setLevel(logging.INFO)

INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
INSUFFICIENT_BALANCE = 'INSUFFICIENT_BALANCE'


def error(error_code: str, msg: str):
    log.error(f"{error_code}, {msg}")
    print(msg)
    return {
        "statusCode": 500,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "errorCode": error_code,
            "errorMessage": msg
        })
    }


def success(res: dict):
    # log.error(error_code, msg)
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(
            res
        )
    }


balances = defaultdict(int)
def lambda_handler(event, context):
    log.info(f'Received {event}')
    try:
        body = event.get('body')
        if body is None:
            return error(INTERNAL_SERVER_ERROR, "No body in input")
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body
        try:
            account_from = int(data['accountFrom'])
        except ValueError:
            return error(INTERNAL_SERVER_ERROR, msg='accountFrom was not int')
        try:
            account_to = int(data['accountTo'])
        except ValueError:
            return error(INTERNAL_SERVER_ERROR, msg='accountTo was not int')            
        try:
            amount = int(data['amount'])  # ?!! int or float/double / decimal
        except ValueError:
            return error(INTERNAL_SERVER_ERROR, msg='amount was not int')            

        transaction_type = data['transactionType']
        prev_balance = balances[account_from]

        if transaction_type not in ('CREDIT', 'DEBIT'):
            return error(INTERNAL_SERVER_ERROR,
                         msg=f'Invalid transaction type {transaction_type}')

        if transaction_type == 'CREDIT':
            account_to_debit, account_to_credit = account_from, account_to 
        else:
            account_to_debit, account_to_credit = account_to, account_from

       
        if balances[account_to_credit] < amount:
            return error(INSUFFICIENT_BALANCE, f"Insufficient Balance in {account_to_credit}")
        else:
            balances[account_to_credit] -= amount
            balances[account_to_debit] += amount

        return success({"currentBalance": balances[account_from],  # not sure what type int format double means here. Should use Decimal type.
                        "previousBalance": prev_balance})

    except Exception as e:
        return error(INTERNAL_SERVER_ERROR, msg=f"{str(e)} Internal exception encountered")  # or str(e))

