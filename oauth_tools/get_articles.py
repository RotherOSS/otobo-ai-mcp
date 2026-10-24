import json

from mcp.server.fastmcp.exceptions import ToolError

import otobo

import domain.get_ticket_details

from mcp.server.auth.middleware.auth_context import get_access_token


@otobo.tool(
    annotations = {
        "title"           : "Get articles",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def get_articles(ticket_id: int, article_ids: list[int]) -> str:

    """
    Returns articles of an OTOBO ticket with their content and url.
    Use it for a ticket too long for get_ticket_details, with the IDs of its article_list.
    Request only the articles needed. If they are many, request them in several calls,
    each with articles whose body_tokens in article_list sum up to less than the limit named by get_ticket_details.
    """

    raw = domain.get_ticket_details.do_get_ticket(
        ticket_id,
        all_articles = True,
        bearer       = get_access_token().token
    )

    if not raw:
        raise ToolError(f"Ticket {ticket_id} not found")

    return json.dumps(otobo.select_articles(raw, article_ids), sort_keys=True)
