import json

import otobo

import domain.update_generated_response


@otobo.tool(
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
    Stores an AI generated answer suggestion in the dynamic field OTOBOAI of a ticket article,
    replacing the previous value.
    Without article_id, the last customer article of the ticket is used, if any.

    Args:
        ticket_id: numeric OTOBO ticket ID
        generated_response: the AI generated answer suggestion
        article_id: optional numeric article ID
        otobo_sid: OTOBO session ID used for authentication
    """
    raw = domain.update_generated_response.do_update_article_df( 'OTOBOAI', ticket_id, generated_response, article_id=article_id, sid=otobo_sid)

    return json.dumps(raw, sort_keys=True)
