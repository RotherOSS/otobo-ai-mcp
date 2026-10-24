from mcp.server.fastmcp.exceptions import ToolError

import otobo

import domain.get_ticket_details


@otobo.tool(
    annotations = {
        "title"           : "Get ticket details from OTOBO",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def get_ticket_details(ticket_id: int, include_articles: bool = True, otobo_sid : str = '') -> tuple[str, str | None]:

    """
    Returns the details of an OTOBO ticket, including dynamic fields,
    linked tickets and FAQ items, and optionally its articles.
    If the ticket is too long, article_list gives each article's ID, sender, subject and size,
    but not its content, then use get_articles to read the articles needed.
    The ticket and linked tickets each carry a url to open them in OTOBO.

    Args:
        ticket_id: numeric OTOBO ticket ID
        include_articles: include the articles, default true
        otobo_sid: OTOBO session ID used for authentication
    """
    raw = domain.get_ticket_details.do_get_ticket(ticket_id, all_articles=include_articles, sid=otobo_sid)

    if not raw:
        raise ToolError(f"Ticket {ticket_id} not found")

    return otobo.filter_ticket(raw, include_articles)

