import json

import otobo

import domain.find_similar_tickets

from mcp.server.auth.middleware.auth_context import get_access_token


@otobo.tool(
    annotations = {
        "title"           : "Find similar tickets",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def find_similar_tickets(ticket_id: int, article_id: int | None = None) -> str:

    """
    Finds OTOBO tickets similar to a ticket by vector similarity.
    Returns {"similar_tickets": [ticket IDs]}, empty if none are found.

    Args:
        article_id: compare only this article of the ticket
    """

    raw = domain.find_similar_tickets.do_find_similar_tickets(
        ticket_id  = ticket_id,
        article_id = article_id,
        bearer     = get_access_token().token
    )

    return json.dumps(raw, sort_keys=True)
