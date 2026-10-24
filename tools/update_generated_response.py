import json

import otobo

import domain.update_generated_response


@otobo.tool(
    confirmation = "Store the following generated response in ticket {ticket_id}, article {article_id} (None meaning the last customer article)?\n\n{generated_response}",
    annotations = {
        "title"           : "Store generated response",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : True,
        "openWorldHint"   : False,
    }
)
def update_generated_response(otobo_sid: str, ticket_id: int, generated_response: str, article_id: int | None = None) -> str:

    """
    Stores an AI generated reply suggestion in the dynamic field OTOBOAI of an OTOBO article,
    replacing its previous value.

    Args:
        otobo_sid: OTOBO session ID
        generated_response: reply text without salutation and closing phrase
        article_id: article to store it in, default the last customer article
    """

    raw = domain.update_generated_response.do_update_article_df( 'OTOBOAI', ticket_id, generated_response, article_id=article_id, sid=otobo_sid)

    return json.dumps(raw, sort_keys=True)
