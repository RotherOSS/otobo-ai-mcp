
import os
import sys
import json
import logging

from typing import Any

import otobo
import rest


def do_transfer_ticket(ticket_id: int, destination_queue: str, sid: str = "") -> bool:

    payload = {
        'SessionID' : sid,
        'Ticket' : {
            "Queue" : destination_queue
        }
    }

    data = rest.put_operation(
        "Ticket/" + str(ticket_id),
        payload
    )

    return data


