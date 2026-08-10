
import os
import sys
import json
import logging

from typing import Any

import otobo
import rest


def do_get_ticket(ticket_id: int, all_articles: bool = True, sid: str = "") -> dict:

    data = rest.get_operation(
        "Ticket/" + str(ticket_id),
        {
            "AllArticles": "1" if all_articles else "0",
            "DynamicFields": "1",
            "Links" : [ "Ticket", "FAQ"  ],
            "SessionID" : sid,
        }
    )

    tickets = data.get("ticket", [])

    if isinstance(tickets, dict):
        return tickets

    if isinstance(tickets, list) and tickets:
        return tickets[0]

    return {}


