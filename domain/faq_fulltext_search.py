
import os
import sys
import json
import logging

from typing import Any

import otobo
import rest


def do_faq_fulltext_search( search_term: str, max_number_of_results: int, bearer:str = None, sid:str = None) -> str:

    payload = {
        'Fulltext'     : search_term,
        "Limit"        : max_number_of_results
    }

    data = rest.get_operation(
        "FAQ",
        payload,
        bearer = bearer,
        sid    = sid,
    )

    data = data.get("faq")

    if isinstance(data,dict):
        data = [ data ]

    for item in data:

        if item.get("faq_id") is not None:
            item["url"] = otobo.settings.faq_url(item["faq_id"])

    return data


