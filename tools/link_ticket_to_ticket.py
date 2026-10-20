import json

from typing import Literal

import otobo

import domain.link_ticket_to_ticket


@otobo.tool(
    annotations = {
        "title"           : "Add a link to another OTOBO Ticket",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def link_ticket_to_ticket( ticket_id: str, linked_ticket_id: str, otobo_sid : str = '', dir: Literal["Normal", "ParentChild"] = 'Normal'  ) -> str:

    """
    Links an OTOBO ticket to another OTOBO ticket.

    Args:
        ticket_id: source ticket of the link, the parent for link type ParentChild
        linked_ticket_id: target ticket of the link, the child for link type ParentChild
        otobo_sid: OTOBO session ID used for authentication
        dir: link type, default 'Normal'
    """

    raw = domain.link_ticket_to_ticket.do_link_ticket( type='Ticket', ticket_id=ticket_id, linked_ticket_id=linked_ticket_id, linked_faq_id=None, sid=otobo_sid, dir=dir)

    return json.dumps(raw, sort_keys=True)

