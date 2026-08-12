import json
import logging

from typing import Any

import otobo
import rest

import domain.unlink_ticket_to_ticket

from mcp.server.auth.middleware.auth_context import get_access_token

@rest.HandleAPIError
@otobo.server.tool(
    annotations = {
        "title"           : "remove a link to another OTOBO Ticket",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : True,
        "openWorldHint"   : False,
    }
)

def unlink_ticket_from_ticket( ticket_id: str, linked_ticket_id: str, dir: str = 'Normal'  ) -> str:

    """
    Delete a link to another OTOBO Ticket or FAQ

    Args:
        ticket_id : ticket to link from
        linked_ticket_id : ticket id to link to
        linked_faq_id : faq id to link to
        dir : link type, default to 'Normal'
    """

    raw = domain.unlink_ticket_to_ticket.do_unlink_ticket( 
        type             = 'Ticket', 
        ticket_id        = ticket_id, 
        linked_ticket_id = linked_ticket_id, 
        linked_faq_id    = None, 
        dir              = dir,
        bearer           = get_access_token().token
    )

    if not raw:
        log.warning( f"Empty search result" )
        return json.dumps({"error": f"Empty search result"})

    return json.dumps(raw)

