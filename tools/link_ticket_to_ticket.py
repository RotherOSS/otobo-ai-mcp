import json
import logging

from typing import Any

import otobo
import rest

import domain.link_ticket_to_ticket


@rest.HandleAPIError
@otobo.server.tool(
    annotations = {
        "title"           : "Add a link to another OTOBO Ticket",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)

def link_ticket_to_ticket( ticket_id: str, linked_ticket_id: str, otobo_sid : str = '', dir: str = 'Normal'  ) -> str:

    """
    Link an OTOBO ticket to another OTOBO Ticket

    Args:
        ticket_id : ticket to link from
        linked_ticket_id : ticket to link to
        otobo_sid: the OTOBO sessionID
        dir : link type, default to 'Normal'
    """
        
    raw = domain.link_ticket_to_ticket.do_link_ticket( type='Ticket', ticket_id=ticket_id, linked_ticket_id=linked_ticket_id, linked_faq_id=None, sid=otobo_sid, dir=dir)

    if not raw:
        log.warning( f"Empty search result" )
        return json.dumps({"error": f"Empty search result"})

    return json.dumps(raw)


