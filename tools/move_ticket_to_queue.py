import json

import otobo

import domain.move_ticket_to_queue


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
def move_ticket_to_queue(otobo_sid: str, ticket_id: int, destination_queue: str) -> str:

    """
    Moves an OTOBO ticket to another queue.

    Args:
        otobo_sid: OTOBO session ID
        destination_queue: queue name
    """

    raw = domain.move_ticket_to_queue.do_move_ticket( ticket_id, destination_queue, sid=otobo_sid)

    return json.dumps(raw, sort_keys=True)
