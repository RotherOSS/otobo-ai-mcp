
import os
import sys
import json
import logging

from typing import Any

import otobo
import rest


def do_find_similar_tickets( ticket_id: str, article_id: str | None, bearer:str = None, sid:str = None ):

    payload = {}

    if article_id is not None:
        payload["ArticleID"] = article_id

    data = {}

    raw = rest.get_operation(
        "Ticket/" + str(ticket_id) + "/Embeddings/ticket_pairs",
        payload,
        sid    = sid,
        bearer = bearer,
    )

    if isinstance(raw, dict):
        raw = [ raw ]

    for item in raw:
        if item["metadata"] is not None:
            metadata = item["metadata"]
            if metadata["source_id"] is not None:
                data[metadata["source_id"]] = 1

    raw = rest.get_operation(
        "Ticket/" + str(ticket_id) + "/Embeddings/ticket_chunks",
        payload,
        sid    = sid,
        bearer = bearer,
    )

    if isinstance(raw, dict):
        raw = [ raw ]

    for item in raw:
        if item["metadata"] is not None:
            metadata = item["metadata"]
            if metadata["source_id"] is not None:
                data[metadata["source_id"]] = 1

    result = []
    for k,v in data.items():
        result.append(k)

    return { "similar_tickets" : result }


