import requests

HOST = "https://api-sandbox.rebilly.com"


def __get_headers(jwt=None, secret_key=None):
    headers = {
        "Accepts": "application/json",
        "Content-Type": "application/json",
    }

    if jwt is not None:
        headers["Authorization"] = "Bearer " + jwt

    if secret_key is not None:
        headers["REB-APIKEY"] = secret_key

    return headers


def get(url, jwt=None, secret_key=None):
    return requests.get(HOST + url, headers=__get_headers(jwt=jwt, secret_key=secret_key), allow_redirects=False)


def put(url, body, jwt=None, secret_key=None):
    return requests.put(HOST + url, json=body, headers=__get_headers(jwt=jwt, secret_key=secret_key), allow_redirects=False)


def post(url, body, jwt=None, secret_key=None):
    return requests.post(HOST + url, json=body, headers=__get_headers(jwt=jwt, secret_key=secret_key), allow_redirects=False)
