import json

import otobo


@otobo.tool(
    annotations = {
        "title"           : "Get a direct link for a ticket in OTOBO",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    })
def get_link_to_ticket(ticket_id: int) -> str:
    """
    Returns the HTTP URL that opens the given ticket in the OTOBO agent interface.

    Args:
        ticket_id: numeric OTOBO ticket ID
    """

    return json.dumps( otobo.settings.ticket_url(ticket_id) )
