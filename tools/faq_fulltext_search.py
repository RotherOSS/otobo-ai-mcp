import json

import otobo

import domain.faq_fulltext_search


@otobo.tool(
    annotations = {
        "title"           : "Search FAQ items",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def faq_fulltext_search(otobo_sid: str, search_term: str, limit: int = 10) -> str:

    """
    Searches OTOBO FAQ items by fulltext.
    Returns the matching FAQ items with their url, or an empty list.

    Args:
        otobo_sid: OTOBO session ID
        limit: maximum number of FAQ items
    """

    raw = domain.faq_fulltext_search.do_faq_fulltext_search( search_term, limit, sid=otobo_sid)

    return json.dumps(raw, sort_keys=True)
