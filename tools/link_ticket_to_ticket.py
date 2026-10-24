import json

from typing import Literal

import otobo

import domain.link_ticket_to_ticket


@otobo.tool(
    confirmation = "Link ticket {ticket_id} to ticket {linked_ticket_id} with link type '{link_type}'?",
    annotations = {
        "title"           : "Link tickets",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def link_ticket_to_ticket(otobo_sid: str, ticket_id: int, linked_ticket_id: int, link_type: Literal["Normal", "ParentChild"] = 'Normal') -> str:

    """
    Links two OTOBO tickets.

    Args:
        otobo_sid: OTOBO session ID
        link_type: Normal links equal tickets, ParentChild makes ticket_id the parent of linked_ticket_id
    """

    raw = domain.link_ticket_to_ticket.do_link_ticket( ticket_id, linked_ticket_id, link_type, sid=otobo_sid)

    return json.dumps(raw, sort_keys=True)
