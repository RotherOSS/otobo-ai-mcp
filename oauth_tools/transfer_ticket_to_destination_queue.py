import json

import otobo

import domain.transfer_ticket_to_destination_queue

from mcp.server.auth.middleware.auth_context import get_access_token

@otobo.tool(
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
    Moves an OTOBO ticket to another queue.

    Args:
        ticket_id: numeric OTOBO ticket ID
        destination_queue: name of the destination queue
    """

    raw = domain.transfer_ticket_to_destination_queue.do_transfer_ticket( 
        ticket_id, 
        destination_queue, 
        bearer = get_access_token().token
    )

    return json.dumps(raw, sort_keys=True)

