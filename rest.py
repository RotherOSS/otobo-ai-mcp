
import os
import sys
import json
import logging
import requests

from typing import Any

import otobo


# OTOBO REST API calls

class APIError(Exception):
    pass
    

# decorator
def HandleAPIError(fun):

    def inner(*args,**kwargs):

        if not otobo.settings.internal_url:
            return json.dumps({"error": "OTOBO_HOST is not configured"})

        result = None
        try:
            result = fun(*args,**kwargs)
        except APIError as e:
            otobo.log.warning( str(e) )
            return json.dumps({"error": str(e)})

        return result


    return inner
    


def post_operation(operation: str, payload: dict) -> dict:

    url = otobo.settings.operation_url(operation)

    otobo.log.debug( f"POST url: {url}")

    try:
        resp = requests.post(
            url,
            headers = {"Content-Type": "application/json"},
            data    = json.dumps(payload),
            verify  = otobo.settings.ssl_verify,
            timeout = otobo.settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {e}") from e

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    return data


def put_operation(operation: str, payload: dict) -> dict:

    url = otobo.settings.operation_url(operation)

    otobo.log.debug( f"PUT url: {url}")

    try:
        resp = requests.put(
            url,
            headers = {"Content-Type": "application/json"},
            data    = json.dumps(payload),
            verify  = otobo.settings.ssl_verify,
            timeout = otobo.settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {e}") from e

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    return data


def get_operation(operation: str, payload: dict) -> dict:

    url = otobo.settings.operation_url(operation)
    otobo.log.debug( f"GET url: {url}, {payload}")

    try:
        resp = requests.get(
            url, headers={ "Content-Type": "application/json" },
            params  = payload,
            verify  = otobo.settings.ssl_verify,
            timeout = otobo.settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {e}") from e

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if isinstance(data,dict) and data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    return data


def delete_operation(operation: str, payload: dict) -> dict:

    url = otobo.settings.operation_url(operation)
    otobo.log.debug( f"DELETE url: {url}, {payload}")

    try:
        resp = requests.delete(
            url, headers={ "Content-Type": "application/json" },
            params  = payload,
            verify  = otobo.settings.ssl_verify,
            timeout = otobo.settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {e}") from e

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    return data


