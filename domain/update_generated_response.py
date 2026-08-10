
import json
import logging
import requests

from typing import Any
#from mcp.server.fastmcp import FastMCP
#from mcp.server.transport_security import TransportSecuritySettings

import otobo
import rest


def do_update_article_df( dfname: str, ticket_id: int, generated_response: str, article_id: int, sid:str) -> dict:

    payload = {
        'SessionID'    : sid,
        'DynamicField' : {
            'Name'  : 'OTOBOAI',
            'Value' : generated_response
        }
    }

    if article_id is not None:
        payload['ArticleID'] = article_id

    data = rest.put_operation(
        "Ticket/" + str(ticket_id) + "/Article/DF",
        payload
    )

    return data

