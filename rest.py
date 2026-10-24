import json
import requests

import otobo


# OTOBO REST API calls

class APIError(Exception):
    pass


# error messages of requests may contain the URL, which carries the SessionID of GET requests
def masked_sid(text: str, sid: str = None) -> str:
    return text.replace(sid, "***") if sid else text


# GET and DELETE send the payload as URL parameters, PUT as JSON body.

def request(method: str, operation: str, payload: dict, sid: str = None, bearer: str = None) -> dict:

    url = otobo.settings.operation_url(operation)
    otobo.log.debug("%s %s %s", method, url, otobo.masked(payload))

    headers = {"Content-Type": "application/json"}
    if bearer is not None:
        headers["Authorization"] = "bearer " + bearer
    elif sid is not None:
        payload["SessionID"] = sid

    if method in ("GET", "DELETE"):
        payload_kwargs = { "params": payload }
    else:
        payload_kwargs = { "data": json.dumps(payload) }

    try:
        resp = requests.request(
            method,
            url,
            headers = headers,
            verify  = otobo.settings.ssl_verify,
            timeout = otobo.settings.timeout,
            **payload_kwargs,
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {masked_sid(str(e), sid)}") from e

    otobo.log.debug("response %s: %s", resp.status_code, resp.text)

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if isinstance(data, dict) and data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    return data


def get_operation(operation: str, payload: dict, sid: str = None, bearer: str = None) -> dict:
    return request("GET", operation, payload, sid=sid, bearer=bearer)


def put_operation(operation: str, payload: dict, sid: str = None, bearer: str = None) -> dict:
    return request("PUT", operation, payload, sid=sid, bearer=bearer)


def delete_operation(operation: str, payload: dict, sid: str = None, bearer: str = None) -> dict:
    return request("DELETE", operation, payload, sid=sid, bearer=bearer)
