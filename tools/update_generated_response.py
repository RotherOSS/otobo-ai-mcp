import json
import logging

from typing import Any

import otobo
import rest

import domain.update_generated_response


@rest.HandleAPIError
@otobo.server.tool(
    annotations = {
        "title"           : "Update generated ticket response in OTOBO",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : True,
        "openWorldHint"   : False,
    }
)
def update_generated_response(ticket_id: int, generated_response: str, article_id: int = None, otobo_sid : str = '') -> str:

    """
    Update the AI generated RAG response of an OTOBO ticket article. if no article id is passed, the last customer article of the ticket is used, if any.

    Args:
        ticket_id: Numeric OTOBO ticket ID.
        generated_response: the AI generated response to store
        article_id: optional article_id
        otobo_sid: the OTOBO sessionID
    """
    raw = domain.update_generated_response.do_update_article_df( 'OTOBO-AI', ticket_id, generated_response, article_id=article_id, sid=otobo_sid)

    if not raw:
        log.warning( f"Ticket {ticket_id} not found" )
        return json.dumps({"error": f"Ticket {ticket_id} not found"})

    return json.dumps(raw)

