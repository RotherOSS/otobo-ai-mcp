import json

import otobo


@otobo.tool(
    annotations = {
        "title"           : "Get a direct link to a FAQ in OTOBO",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    })
def get_link_to_faq(faq_id: int) -> str:
    """
    Returns the HTTP URL that opens the given FAQ item in the OTOBO agent interface.

    Args:
        faq_id: numeric OTOBO FAQ item ID
    """

    return json.dumps( otobo.settings.faq_url(faq_id) )




