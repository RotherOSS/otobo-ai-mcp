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
def get_articles(ticket_id: int, article_ids: list[int]) -> tuple[str, str | None]:

    """
    Returns the content and url of the given articles of an OTOBO ticket.
    Use the article IDs of the article_list of get_ticket_details.
    """

    raw = domain.get_ticket_details.do_get_ticket(
        ticket_id,
        all_articles = True,
        bearer       = get_access_token().token
    )

    if not raw:
        raise ToolError(f"Ticket {ticket_id} not found")

    return otobo.select_articles(raw, article_ids)
