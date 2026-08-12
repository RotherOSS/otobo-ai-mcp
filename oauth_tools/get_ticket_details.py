import json
import logging

from typing import Any

import otobo
import rest

import domain.get_ticket_details     

from mcp.server.auth.middleware.auth_context import get_access_token

@rest.HandleAPIError
@otobo.server.tool(
    annotations = {
        "title"           : "Get ticket details from OTOBO",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def get_ticket_details(ticket_id: int, include_articles: bool = True) -> str:

    """
    Get full details of an OTOBO ticket by ID, including dynamic fields and optionally all articles.

    Args:
        ticket_id: Numeric OTOBO ticket ID.
        include_articles: Include articles/comments, default true.
    """
    raw = domain.get_ticket_details.do_get_ticket(
        ticket_id, 
        all_articles = include_articles, 
        bearer       = get_access_token().token
    )

    if not raw:
        log.warning( f"Ticket {ticket_id} not found" )
        return json.dumps({"error": f"Ticket {ticket_id} not found"})

    return json.dumps(otobo.filter_ticket(raw, include_articles))


