import json

from mcp.server.fastmcp.exceptions import ToolError

import otobo

import domain.get_ticket_details

from mcp.server.auth.middleware.auth_context import get_access_token

@otobo.tool(
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
    Returns the details of an OTOBO ticket, including dynamic fields,
    linked tickets and FAQ items, and optionally all articles.
    The ticket, its articles and linked tickets each carry a url to open them in OTOBO.

    Args:
        ticket_id: numeric OTOBO ticket ID
        include_articles: include all articles, default true
    """
    raw = domain.get_ticket_details.do_get_ticket(
        ticket_id, 
        all_articles = include_articles, 
        bearer       = get_access_token().token
    )

    if not raw:
        raise ToolError(f"Ticket {ticket_id} not found")

    return json.dumps(otobo.filter_ticket(raw, include_articles))


