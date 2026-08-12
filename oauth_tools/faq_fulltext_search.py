
import json
import logging

from typing import Any

import otobo
import rest

import domain.faq_fulltext_search

from mcp.server.auth.middleware.auth_context import get_access_token

@rest.HandleAPIError
@otobo.server.tool(
    annotations = {
        "title"           : "Do a FAQ fulltext search",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def faq_fulltext_search( search_term: str, max_number_of_results: int = 10  ) -> str:

    """
    Do a fulltext search in OTOBO FAQs for the given search query term.

    Args:
        search_term: the search query term
        destination_queue: Name of the destination queue
    """
    
            
    raw = domain.faq_fulltext_search.do_faq_fulltext_search( 
        search_term, 
        max_number_of_results, 
        bearer = get_access_token().token
    )

    if not raw:
        log.warning( f"Empty search result" )
        return json.dumps({"error": f"Empty search result"})

    return json.dumps(raw)


