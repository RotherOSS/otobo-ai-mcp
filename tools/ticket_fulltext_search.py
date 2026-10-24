import json

import otobo

import domain.ticket_fulltext_search


@otobo.tool(
    annotations = {
        "title"           : "Search tickets",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def ticket_fulltext_search(otobo_sid: str, search_term: str, limit: int = 10) -> str:

    """
    Searches OTOBO tickets by fulltext.
    Returns the matching tickets with their url, or an empty list.

    Args:
        otobo_sid: OTOBO session ID
        limit: maximum number of tickets
    """

    raw = domain.ticket_fulltext_search.do_ticket_fulltext_search( search_term, limit, sid=otobo_sid)

    return json.dumps(raw, sort_keys=True)
