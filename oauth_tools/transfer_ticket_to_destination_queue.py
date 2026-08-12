import json
import logging

from typing import Any

import otobo
import rest

import domain.transfer_ticket_to_destination_queue

from mcp.server.auth.middleware.auth_context import get_access_token

@rest.HandleAPIError
@otobo.server.tool(
    annotations = {
        "title"           : "Transfer ticket to destination queue in OTOBO",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : True,
        "openWorldHint"   : False,
    }
)
def transfer_ticket_to_destination_queue(ticket_id: int, destination_queue: str ) -> str:

    """
    Move Ticket to new destination queue.

    Args:
        ticket_id: Numeric OTOBO ticket ID.
        destination_queue: Name of the destination queue
    """

    raw = domain.transfer_ticket_to_destination_queue.do_transfer_ticket( 
        ticket_id, 
        destination_queue, 
        bearer = get_access_token().token
    )

    if not raw:
        log.warning( f"Ticket {ticket_id} not found" )
        return json.dumps({"error": f"Ticket {ticket_id} not found"})

    return json.dumps(raw)

