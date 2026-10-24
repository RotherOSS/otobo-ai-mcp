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
def find_similar_tickets(otobo_sid: str, ticket_id: int, article_id: int | None = None) -> str:

    """
    Finds OTOBO tickets similar to a ticket by vector similarity.
    Returns {"similar_tickets": [ticket IDs]}, empty if none are found.

    Args:
        otobo_sid: OTOBO session ID
        article_id: compare only this article of the ticket
    """

    raw = domain.find_similar_tickets.do_find_similar_tickets( ticket_id=ticket_id, article_id=article_id, sid=otobo_sid)

    return json.dumps(raw, sort_keys=True)
