import json

from mcp.server.fastmcp.exceptions import ToolError

import otobo

import domain.get_ticket_details

from mcp.server.auth.middleware.auth_context import get_access_token

@otobo.tool(
    annotations = {
        "title"           : "Get articles of a ticket from OTOBO",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def get_articles(ticket_id: int, article_ids: list[int]) -> str:

    """
    Returns the articles of an OTOBO ticket including their content,
    each with a url to open it in OTOBO.
    Use it to read the articles of a ticket too long for get_ticket_details to return them in full.
    The articles are selected by their IDs as listed in article_list by get_ticket_details.
    Request all articles needed in a single call, eg [250722, 250723, 250726],
    rather than calling this tool once per article.

    Args:
        ticket_id: numeric OTOBO ticket ID
        article_ids: numeric OTOBO article IDs of the articles to return
    """
    raw = domain.get_ticket_details.do_get_ticket(
        ticket_id,
        all_articles = True,
        bearer       = get_access_token().token
    )

    if not raw:
        raise ToolError(f"Ticket {ticket_id} not found")

    return json.dumps(otobo.select_articles(raw, article_ids), sort_keys=True)
