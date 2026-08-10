import json
import logging

from typing import Any

import otobo
import rest


@otobo.server.tool(
    annotations = {
        "title"           : "Get a direct link for a ticket in OTOBO",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    })
def get_link_to_ticket(ticket_id: int) -> str:
    """
    Get a valid HTTP link to browse to a specific ticket_id in OTOBO.

    Args:
        ticket_id: Numeric OTOBO ticket ID.
    """

    return json.dumps( otobo.settings.ticket_url(ticket_id) )


