
import json
import logging
import requests

from typing import Any

import otobo
import rest


def do_update_article_df( dfname: str, ticket_id: int, generated_response: str, article_id: int, sid:str = None, bearer:str = None) -> dict:

    payload = {
        'DynamicField' : {
            'Name'  : 'OTOBOAI',
            'Value' : generated_response
        }
    }

    if article_id is not None:
        payload['ArticleID'] = article_id

    data = rest.put_operation(
        "Ticket/" + str(ticket_id) + "/Article/DF",
        payload,
        sid    = sid,
        bearer = bearer,
    )

    return data

