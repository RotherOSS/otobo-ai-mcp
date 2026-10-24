import json

from typing import Literal

import otobo

import domain.unlink_ticket_from_ticket


@otobo.tool(
    confirmation = "Remove the link of type '{link_type}' between ticket {ticket_id} and ticket {linked_ticket_id}?",
    annotations = {
        "title"           : "Unlink tickets",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : True,
        "openWorldHint"   : False,
    }
)
def unlink_ticket_from_ticket(otobo_sid: str, ticket_id: int, linked_ticket_id: int, link_type: Literal["Normal", "ParentChild"] = 'Normal') -> str:

    """
    Removes the link between two OTOBO tickets.

    Args:
        otobo_sid: OTOBO session ID
        link_type: Normal links equal tickets, ParentChild makes ticket_id the parent of linked_ticket_id
    """

    raw = domain.unlink_ticket_from_ticket.do_unlink_ticket( ticket_id, linked_ticket_id, link_type, sid=otobo_sid)

    return json.dumps(raw, sort_keys=True)
