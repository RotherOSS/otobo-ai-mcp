
import os
import sys
import json
import logging

from typing import Any

import otobo
import rest


def do_link_ticket( type: str, ticket_id: str, linked_ticket_id: str, linked_faq_id: str, dir : str, sid : str = None, bearer : str = None ) -> str:

    payload = {}

    target = "Ticket" if linked_ticket_id is not None else "FAQ"
    target_id = linked_ticket_id if linked_ticket_id is not None else linked_faq_id

    data = rest.put_operation(
        "Ticket/" + str(ticket_id) + "/Link/" + target + "/" + str(dir) + "/" + str(linked_ticket_id),
        payload,
        sid    = sid,
        bearer = bearer,
    )

    return data


