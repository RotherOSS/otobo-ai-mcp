from mcp.server.fastmcp.exceptions import ToolError

import otobo

import domain.get_ticket_details


@otobo.tool(
    annotations = {
        "title"           : "Get ticket details",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def get_ticket_details(otobo_sid: str, ticket_id: int, include_articles: bool = True) -> tuple[str, str | None]:

    """
    Returns an OTOBO ticket with its dynamic fields, linked tickets and FAQ items,
    and optionally its articles, each with their url.
    If the ticket is too long, article_list lists the articles without content,
    read them with get_articles.

    Args:
        otobo_sid: OTOBO session ID
    """

    raw = domain.get_ticket_details.do_get_ticket(ticket_id, all_articles=include_articles, sid=otobo_sid)

    if not raw:
        raise ToolError(f"Ticket {ticket_id} not found")

    return otobo.filter_ticket(raw, include_articles)
