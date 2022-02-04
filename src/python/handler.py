import os
import json
import logging
from decimal import Decimal
from collections import defaultdict

import requests

log = logging.getLogger()
log.setLevel(logging.INFO)


VALIDATION_ERROR = "VALIDATION_ERROR"
INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE"

cb_url = os.getenv("CORE_BANKING_BASE_URL", "http://corebanking-dev.com")


def call_core_banking(data: dict):
    headers = {}  # to be defined
    return requests.post(cb_url + "/transactions", headers=headers, data=data)


def error(error_code: str, msg: str):
    return {
        "statusCode": 500,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"errorCode": error_code, "errorMessage": msg}),
    }


def success(res: dict):
    # log.error(error_code, msg)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(res["body"]),
    }


def lambda_handler(event, context):
    """ 
    Lambda Function takes in an input event and forwards it to the Core Banking
    API after validating inputs. Follows the core banking API in its return sig
    """
    log.info(f"Received {event}")
    try:
        body = event.get("body")
        if body is None:
            return error(VALIDATION_ERROR, "No body in input")

        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body
        try:
            account_from = int(data["account_from"])
        except ValueError:
            return error(VALIDATION_ERROR, msg="account_from was not int")
        except KeyError:
            return error(VALIDATION_ERROR, msg="account_from was not present")
        try:
            account_to = int(data["account_to"])
        except ValueError:
            return error(VALIDATION_ERROR, msg="account_to was not int")
        except KeyError:
            return error(VALIDATION_ERROR, msg="account_to was not present")
        try:
            amount = int(data["amount"])  # ?!! int or float/double / decimal
            if amount <= 0:
                return error(VALIDATION_ERROR, msg="amount was <= 0")
        except ValueError:
            return error(VALIDATION_ERROR, msg="amount was not int")
        except KeyError:
            return error(VALIDATION_ERROR, msg="amount was not present")

        d = {
            "accountFrom": account_from,
            "accountTo": account_to,
            "amount": amount,
            "transactionType": "DEBIT",
        }

        response = call_core_banking(d)

        if response.status_code == 200:
            return success(response.json())
        elif response.status_code == 500:
            data = response.json()
            return error(data["body"]["errorCode"], data["body"]["errorMessage"])
        else:
            raise NotImplementedError(
                f"Unexpected status_code from api {response.status_code}"
            )

    except Exception as e:
        log.error(str(e))
        return error(
            INTERNAL_SERVER_ERROR, msg=str(e) + f"Internal exception encountered"
        )
