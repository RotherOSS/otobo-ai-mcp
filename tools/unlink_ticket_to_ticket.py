import json

from typing import Literal

import otobo

import domain.unlink_ticket_to_ticket


@otobo.server.tool(
    annotations = {
        "title"           : "Remove a link to another OTOBO Ticket",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : True,
        "openWorldHint"   : False,
    }
)
def unlink_ticket_from_ticket( ticket_id: str, linked_ticket_id: str, otobo_sid : str = '', dir: Literal["Normal", "ParentChild"] = 'Normal'  ) -> str:

    """
    Removes the link between two OTOBO tickets.

    Args:
        ticket_id: source ticket of the link, the parent for link type ParentChild
        linked_ticket_id: target ticket of the link, the child for link type ParentChild
        otobo_sid: OTOBO session ID used for authentication
        dir: link type, default 'Normal'
    """

    raw = domain.unlink_ticket_to_ticket.do_unlink_ticket( type='Ticket', ticket_id=ticket_id, linked_ticket_id=linked_ticket_id, linked_faq_id=None, sid=otobo_sid, dir=dir)

    return json.dumps(raw)
