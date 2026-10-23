
import json
import requests

import otobo


# OTOBO REST API calls

class APIError(Exception):
    pass


# error messages of requests may contain the URL, which carries the SessionID of GET requests
def masked_sid(text: str, sid: str = None) -> str:
    return text.replace(sid, "***") if sid else text


def post_operation(operation: str, payload: dict, bearer:str = None, sid:str = None) -> dict:

    url = otobo.settings.operation_url(operation)

    otobo.log.debug("POST %s %s", url, otobo.masked(payload))

    headers = {"Content-Type": "application/json"}
    if bearer is not None:
        headers["Authorization"] = "bearer " + bearer
    elif sid is not None:
        payload["SessionID"] = sid

    try:
        resp = requests.post(
            url,
            headers = headers,
            data    = json.dumps(payload),
            verify  = otobo.settings.ssl_verify,
            timeout = otobo.settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {masked_sid(str(e), sid)}") from e

    otobo.log.debug("response %s: %s", resp.status_code, resp.text)

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    return data


def put_operation(operation: str, payload: dict, bearer:str = None, sid:str = None) -> dict:

    url = otobo.settings.operation_url(operation)

    otobo.log.debug("PUT %s %s", url, otobo.masked(payload))

    headers = {"Content-Type": "application/json"}
    if bearer is not None:
        headers["Authorization"] = "bearer " + bearer
    elif sid is not None:
        payload["SessionID"] = sid

    try:
        resp = requests.put(
            url,
            headers = headers,
            data    = json.dumps(payload),
            verify  = otobo.settings.ssl_verify,
            timeout = otobo.settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {masked_sid(str(e), sid)}") from e

    otobo.log.debug("response %s: %s", resp.status_code, resp.text)

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    return data


def get_operation(operation: str, payload: dict, bearer:str = None, sid:str = None) -> dict:

    url = otobo.settings.operation_url(operation)
    otobo.log.debug("GET %s %s", url, otobo.masked(payload))

    headers = {"Content-Type": "application/json"}
    if bearer is not None:
        headers["Authorization"] = "bearer " + bearer
    elif sid is not None:
        payload["SessionID"] = sid

    try:
        resp = requests.get(
            url,
            headers = headers,
            params  = payload,
            verify  = otobo.settings.ssl_verify,
            timeout = otobo.settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {masked_sid(str(e), sid)}") from e

    otobo.log.debug("response %s: %s", resp.status_code, resp.text)

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if isinstance(data,dict) and data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    return data


def delete_operation(operation: str, payload: dict, bearer:str = None, sid:str = None) -> dict:

    url = otobo.settings.operation_url(operation)
    otobo.log.debug("DELETE %s %s", url, otobo.masked(payload))

    headers = {"Content-Type": "application/json"}
    if bearer is not None:
        headers["Authorization"] = "bearer " + bearer
    elif sid is not None:
        payload["SessionID"] = sid

    try:
        resp = requests.delete(
            url,
            headers = headers,
            params  = payload,
            verify  = otobo.settings.ssl_verify,
            timeout = otobo.settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {masked_sid(str(e), sid)}") from e

    otobo.log.debug("response %s: %s", resp.status_code, resp.text)

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    return data


