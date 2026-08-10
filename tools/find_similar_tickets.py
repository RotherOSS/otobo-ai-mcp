import json
import logging

from typing import Any

import otobo
import rest

import domain.find_similar_tickets


@rest.HandleAPIError
@otobo.server.tool(
    annotations = {
        "title"           : "Find similar tickets",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def find_similar_tickets( ticket_id: str, otobo_sid : str = '', article_id : str | None = None ) -> str:

    """
    Find similar tickets to this one.

    Args:
        ticket_id : the ticket id
        article_id : the article id
        otobo_sid: the OTOBO sessionID
    """
        
    raw = domain.find_similar_tickets.do_find_similar_tickets( ticket_id=ticket_id, article_id=article_id, sid=otobo_sid)

    if not raw:
        log.warning( f"Empty search result" )
        return json.dumps({"error": f"Empty search result"})

    return json.dumps(raw)


