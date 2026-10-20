import json

import otobo

import domain.transfer_ticket_to_destination_queue


@otobo.tool(
    annotations = {
        "title"           : "Transfer ticket to destination queue in OTOBO",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : True,
        "openWorldHint"   : False,
    }
)
def transfer_ticket_to_destination_queue(ticket_id: int, destination_queue: str, otobo_sid : str = '') -> str:

    """
    Moves an OTOBO ticket to another queue.

    Args:
        ticket_id: numeric OTOBO ticket ID
        destination_queue: name of the destination queue
        otobo_sid: OTOBO session ID used for authentication
    """

    raw = domain.transfer_ticket_to_destination_queue.do_transfer_ticket( ticket_id, destination_queue, sid=otobo_sid)

    return json.dumps(raw, sort_keys=True)
