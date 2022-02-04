import requests

if __name__ == "__main__":
    data = {"body": {"account_from": "123", "account_to": "456", "amount": "2000"}}
    response = requests.post(
        "http://localhost/2015-03-31/functions/function/invocations", json=data
    )
    print(response, response.status_code, response.json())
