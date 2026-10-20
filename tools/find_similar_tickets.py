import json

import otobo

import domain.find_similar_tickets


@otobo.tool(
    annotations = {
        "title"           : "Find similar tickets",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def find_similar_tickets( ticket_id: str, otobo_sid : str = '', article_id : str | None = None ) -> str:

    """
    Find tickets similar to the given ticket by vector similarity search.
    Returns {"similar_tickets": [...]} with the IDs of the similar tickets,
    which is empty if none are found.

    Args:
        ticket_id: OTOBO ticket ID
        otobo_sid: OTOBO session ID used for authentication
        article_id: optional article ID to restrict the comparison to this article
    """

    raw = domain.find_similar_tickets.do_find_similar_tickets( ticket_id=ticket_id, article_id=article_id, sid=otobo_sid)

    return json.dumps(raw)

