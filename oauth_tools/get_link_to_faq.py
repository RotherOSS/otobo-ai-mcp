import json
import logging

from typing import Any

import otobo
import rest


@otobo.server.tool(
    annotations = {
        "title"           : "Get a direct link to a FAQ in OTOBO",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    })
def get_link_to_faq(faq_id: int) -> str:
    """
    Get a valid HTTP link to browse to a specific faq_id in OTOBO.

    Args:
        faq_id: Numeric OTOBO ticket ID.
    """

    return json.dumps( otobo.settings.faq_url(faq_id) )




