
import json

import otobo

import domain.faq_fulltext_search


@otobo.tool(
    annotations = {
        "title"           : "FAQ fulltext search",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def faq_fulltext_search( search_term: str, otobo_sid : str = '', max_number_of_results: int = 10  ) -> str:

    """
    Fulltext search in OTOBO FAQ items.
    Returns a list of matching FAQ items, each with a url to open it in OTOBO.
    Returns an empty list if nothing matches.

    Args:
        search_term: the search query term
        otobo_sid: OTOBO session ID used for authentication
        max_number_of_results: maximum number of FAQ items returned
    """

    raw = domain.faq_fulltext_search.do_faq_fulltext_search( search_term, max_number_of_results, sid=otobo_sid)

    return json.dumps(raw, sort_keys=True)

