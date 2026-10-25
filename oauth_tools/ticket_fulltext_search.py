import json

import otobo

import domain.ticket_fulltext_search

from mcp.server.auth.middleware.auth_context import get_access_token


@otobo.tool(
    annotations = {
        "title"           : "Search tickets",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def ticket_fulltext_search(search_term: str, limit: int = 10) -> str:

    """
    Searches OTOBO tickets by fulltext.
    Returns the matching tickets with their url, or an empty list.

    Args:
        limit: maximum number of tickets
    """

    raw = domain.ticket_fulltext_search.do_ticket_fulltext_search(
        search_term,
        limit,
        bearer = get_access_token().token
    )

    return json.dumps(raw, sort_keys=True)
