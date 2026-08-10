
import os
import sys
import json
import logging

from typing import Any

import otobo
import rest


def do_ticket_fulltext_search( search_term: str, max_number_of_results: int, sid : str ) -> str:

    payload = {
        'SessionID'    : sid,
        'Fulltext'     : search_term,
        "Limit"        : max_number_of_results
    }

    data = rest.get_operation(
        "Ticket",
        payload
    )

    data = data.get("ticket")

    if isinstance(data,dict):
        data = [ data ]

    for item in data:

        if item.get("ticket_id") is not None:
            item["url"] = otobo.settings.ticket_url( item["ticket_id"] )

    return data

