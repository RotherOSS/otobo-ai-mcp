import json

import otobo

import domain.move_ticket_to_queue

from mcp.server.auth.middleware.auth_context import get_access_token


@otobo.tool(
    confirmation = "Move ticket {ticket_id} to queue '{destination_queue}'?",
    annotations = {
        "title"           : "Move ticket to queue",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : True,
        "openWorldHint"   : False,
    }
)
def move_ticket_to_queue(ticket_id: int, destination_queue: str) -> str:

    """
    Moves an OTOBO ticket to another queue.

    Args:
        destination_queue: queue name
    """

    raw = domain.move_ticket_to_queue.do_move_ticket(
        ticket_id,
        destination_queue,
        bearer = get_access_token().token
    )

    return json.dumps(raw, sort_keys=True)
