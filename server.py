#!/usr/bin/env python3
"""
OTOBO AI MCP Server — interact with OTOBO REST API via MCP

Environment:
    OTOBO_MCP_BIND                 Bind address, default is 0.0.0.0
    OTOBO_MCP_PORT                 MCP server port, default is 8765
    OTOBO_MCP_INTERNAL_URL         Webservice endpoint eg http://web:5000/ when running under Docker
    OTOBO_MCP_PUBLIC_URL           Public base url, eg to point the user's browser to
    OTOBO_MCP_WEBSERVICE    	   Web service name (default: OTOBO-AI)
    OTOBO_MCP_SSL_VERIFY           SSL verification (default: false)
    OTOBO_MCP_TIMEOUT              HTTP timeout in seconds (default: 30)
    OTOBO_MCP_TRANSPORT            Transport: stdio, sse, streamable-http (default: stdio)
    OTOBO_MCP_LOGLEVEL             log level, default: info
"""

import os
import sys
import json
import logging
import requests
import argparse

from typing import Any
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings



# Configuration
class Settings:
    def __init__(self):
        self.bind         = os.environ.get("OTOBO_MCP_BIND", "0.0.0.0")
        self.port         = int(os.environ.get("OTOBO_MCP_PORT", 8765))
        self.internal_url = os.environ.get("OTOBO_MCP_INTERNAL_URL", "http://web:5000/").rstrip("/")
        self.public_url   = os.environ.get("OTOBO_MCP_PUBLIC_URL", "https://localhost/otobo/index.pl")
        self.webservice   = os.environ.get("OTOBO_MCP_WEBSERVICE", "OTOBO-AI")
        self.ssl_verify   = os.environ.get("OTOBO_MCP_SSL_VERIFY", "false").lower() in ("true", "1", "yes")
        self.timeout      = int(os.environ.get("OTOBO_MCP_TIMEOUT", 30))
        self.transport    = os.environ.get("OTOBO_MCP_TRANSPORT", "streamable-http")
        self.loglevel     = int(os.environ.get("OTOBO_MCP_LOGLEVEL",40)) # see https://docs.python.org/3/library/logging.html#logging-levels

    def operation_url(self, operation: str) -> str:
        return f"{self.internal_url}/otobo/nph-genericinterface.pl/Webservice/{self.webservice}/{operation}"

    def api_base_url(self) -> str:
        return f"{self.internal_url}/otobo/"

    def ticket_url(self, ticket_id) -> str:
        return f"{self.public_url}?Action=AgentTicketZoom;TicketID={ticket_id}"

    def faq_url(self, faq_id) -> str:
        return f"{self.public_url}?Action=AgentFAQZoom;ItemID={faq_id}"

    def article_url(self,ticket_id,article_id) -> str:
        return f"{self.public_url}?Action=AgentTicketZoom;TicketID={ticket_id};ArticleID={article_id}"


# globals

settings  = Settings()

# logging

log = logging.getLogger("otobo-mcp")
logging.basicConfig(level=settings.loglevel, format="%(asctime)s %(levelname)s %(name)s: %(message)s", stream=sys.stderr)

# server instance 

server    = FastMCP(
    "otobo-mcp-server",
    transport_security = TransportSecuritySettings(
        enable_dns_rebinding_protection = False,
    )
)


# OTOBO REST API calls

class APIError(Exception):
    pass


def post_operation(operation: str, payload: dict) -> dict:

    url = settings.operation_url(operation)

    log.debug( f"POST url: {url}")

    try:
        resp = requests.post(
            url,
            headers = {"Content-Type": "application/json"},
            data    = json.dumps(payload),
            verify  = settings.ssl_verify,
            timeout = settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {e}") from e

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    log.debug(data)
    return data


def put_operation(operation: str, payload: dict) -> dict:

    url = settings.operation_url(operation)

    log.debug( f"PUT url: {url}")

    try:
        resp = requests.put(
            url,
            headers = {"Content-Type": "application/json"},
            data    = json.dumps(payload),
            verify  = settings.ssl_verify,
            timeout = settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {e}") from e

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    log.debug(data)
    return data


def get_operation(operation: str, payload: dict) -> dict:

    url = settings.operation_url(operation)
    log.debug( f"GET url: {url}, {payload}")

    try:
        resp = requests.get(
            url, headers={ "Content-Type": "application/json" },
            params  = payload,
            verify  = settings.ssl_verify,
            timeout = settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {e}") from e

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if isinstance(data,dict) and data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    log.debug(data)
    return data


def delete_operation(operation: str, payload: dict) -> dict:

    url = settings.operation_url(operation)
    log.debug( f"DELETE url: {url}, {payload}")

    try:
        resp = requests.delete(
            url, headers={ "Content-Type": "application/json" },
            params  = payload,
            verify  = settings.ssl_verify,
            timeout = settings.timeout
        )
    except requests.RequestException as e:
        raise APIError(f"Connection error: {e}") from e

    if resp.status_code != 200:
        raise APIError(f"HTTP {resp.status_code}: {resp.reason} - {resp.text[:300]}")

    data = resp.json()
    if data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    log.debug(data)
    return data


# business logic functions that use above OTOBO REST endpoints

def do_get_ticket(ticket_id: int, all_articles: bool = True, sid: str = "") -> dict:

    data = get_operation(
        "Ticket/" + str(ticket_id),
        {
            "AllArticles": "1" if all_articles else "0",
            "DynamicFields": "1",
            "Links" : [ "Ticket", "FAQ"  ],
            "SessionID" : sid,
        }
    )
    tickets = data.get("ticket", [])
    if isinstance(tickets, dict):
        return tickets
    if isinstance(tickets, list) and tickets:
        return tickets[0]
    return {}


def do_transfer_ticket(ticket_id: int, destination_queue: str, sid: str = "") -> bool:

    payload = {
        'SessionID'    : sid,
        'Ticket' : {
            "Queue" : destination_queue
        }
    }

    data = put_operation(
        "Ticket/" + str(ticket_id),
        payload
    )

    return data


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

    data = put_operation(
        "Ticket/" + str(ticket_id) + "/Article/DF",
        payload
    )

    return data


def do_faq_fulltext_search( search_term: str, max_number_of_results: int, sid : str ) -> str:

    payload = {
        'SessionID'    : sid,
        'Fulltext'     : search_term,
        "Limit"        : max_number_of_results
    }

    data = get_operation(
        "FAQ",
        payload
    )

    data = data.get("faq")

    if isinstance(data,dict):
        data = [ data ]

    for item in data:

        if item.get("faq_id") is not None:
            item["url"] = settings.faq_url(item["faq_id"])

    return data


def do_ticket_fulltext_search( search_term: str, max_number_of_results: int, sid : str ) -> str:

    payload = {
        'SessionID'    : sid,
        'Fulltext'     : search_term,
        "Limit"        : max_number_of_results
    }

    data = get_operation(
        "Ticket",
        payload
    )

    data = data.get("ticket")

    if isinstance(data,dict):
        data = [ data ]

    for item in data:

        if item.get("ticket_id") is not None:
            item["url"] = settings.ticket_url( item["ticket_id"] )

    return data


def do_find_similar_tickets( ticket_id: str, article_id: str | None, sid : str ):

    payload = {
        'SessionID'    : sid
    }

    if article_id is not None:
        payload["ArticleID"] = article_id

    data = {}

    raw = get_operation(
        "Ticket/" + str(ticket_id) + "/Embeddings/ticket_pairs",
        payload
    )

    if isinstance(raw, dict):
        raw = [ raw ]

    for item in raw:
        if item["metadata"] is not None:
            metadata = item["metadata"]
            if metadata["source_id"] is not None:
                data[metadata["source_id"]] = 1

    raw = get_operation(
        "Ticket/" + str(ticket_id) + "/Embeddings/ticket_chunks",
        payload
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


def do_link_ticket( type: str, ticket_id: str, linked_ticket_id: str, linked_faq_id: str, sid : str, dir: str ) -> str:

    payload = {
        'SessionID'    : sid,
    }

    target = "Ticket" if linked_ticket_id is not None else "FAQ"
    target_id = linked_ticket_id if linked_ticket_id is not None else linked_faq_id

    data = put_operation(
        "Ticket/" + str(ticket_id) + "/Link/" + target + "/" + str(dir) + "/" + str(linked_ticket_id),
        payload
    )

    return data


def do_unlink_ticket( type: str, ticket_id: str, linked_ticket_id: str, linked_faq_id: str, sid : str, dir: str ) -> str:

    payload = {
        'SessionID'    : sid,
    }

    target = "Ticket" if linked_ticket_id is not None else "FAQ"
    target_id = linked_ticket_id if linked_ticket_id is not None else linked_faq_id

    data = delete_operation(
        "Ticket/" + str(ticket_id) + "/Link/" + target + "/" + str(dir) + "/" + str(linked_ticket_id),
        payload
    )

    return data




# helpers and filters

def fetch_articles(ticket: dict) -> list[dict]:

    articles = ticket.get("article", [])
    if isinstance(articles, dict):
        return [articles]

    for article in articles:
        if article.get("article_id") is not None:
            article["url"] = settings.article_url( ticket["ticket_id"], article["article_id"] )

    return articles


def filter_ticket(ticket: dict, include_articles: bool = True) -> dict:

    log.error(ticket["ticket_id"])
    out = ticket

    out["article"] = fetch_articles(ticket)

    out["url"] = settings.ticket_url(ticket["ticket_id"]) if ticket.get("ticket_id") else None

    if ticket.get("linked") is not None:
        linked = ticket["linked"]
        if isinstance(linked, dict):
            linked = [ linked ];
        for link in linked:
            if link["ticket"] is not None:
                id = link["ticket"]["ticket_id"]
                link["ticket"]["url"] = settings.ticket_url(id)

    log.error(out["url"])
    return out




# the MCP tools available via this MCP

@server.tool(
    annotations = {
        "title"           : "Get ticket details from OTOBO",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def get_ticket_details(ticket_id: int, include_articles: bool = True, otobo_sid : str = '') -> str:

    """
    Get full details of an OTOBO ticket by ID, including dynamic fields and optionally all articles.

    Args:
        ticket_id: Numeric OTOBO ticket ID.
        include_articles: Include articles/comments, default true.
        otobo_sid: the OTOBO sessionID
    """
    if not settings.internal_url:
        return json.dumps({"error": "OTOBO_HOST is not configured"})

    try:
        raw = do_get_ticket(ticket_id, all_articles=include_articles, sid=otobo_sid)
    except APIError as e:
        log.warning( str(e) )
        return json.dumps({"error": str(e)})

    if not raw:
        log.warning( f"Ticket {ticket_id} not found" )
        return json.dumps({"error": f"Ticket {ticket_id} not found"})

    return json.dumps(filter_ticket(raw, include_articles))


@server.tool(
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
    if not settings.internal_url:
        return json.dumps({"error": "OTOBO_HOST is not configured"})

    try:
        raw = do_update_article_df( 'OTOBO-AI', ticket_id, generated_response, article_id=article_id, sid=otobo_sid)
    except APIError as e:
        log.warning( str(e) )
        return json.dumps({"error": str(e)})

    if not raw:
        log.warning( f"Ticket {ticket_id} not found" )
        return json.dumps({"error": f"Ticket {ticket_id} not found"})

    return json.dumps(raw)


@server.tool(
    annotations = {
        "title"           : "Transfer ticket to destination queue in OTOBO",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : True,
        "openWorldHint"   : False,
    }
)
def transfer_ticket_to_destination_queue(ticket_id: int, destination_queue: str, otobo_sid : str = '') -> str:

    """
    Move Ticket to new destination queue.

    Args:
        ticket_id: Numeric OTOBO ticket ID.
        destination_queue: Name of the destination queue
        otobo_sid: the OTOBO sessionID
    """
    if not settings.internal_url:
        return json.dumps({"error": "OTOBO_HOST is not configured"})

    try:
        raw = do_transfer_ticket( ticket_id, destination_queue, sid=otobo_sid)
    except APIError as e:
        log.warning( str(e) )
        return json.dumps({"error": str(e)})

    if not raw:
        log.warning( f"Ticket {ticket_id} not found" )
        return json.dumps({"error": f"Ticket {ticket_id} not found"})

    return json.dumps(raw)

@server.tool(
    annotations = {
        "title"           : "Do a FAQ fulltext search",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def faq_fulltext_search( search_term: str, otobo_sid : str = '', max_number_of_results: int = 10  ) -> str:

    """
    Do a fulltext search in OTOBO FAQs for the given search query term.

    Args:
        search_term: the search query term
        destination_queue: Name of the destination queue
        otobo_sid: the OTOBO sessionID
    """
    if not settings.internal_url:
        return json.dumps({"error": "OTOBO_HOST is not configured"})

    try:
        raw = do_faq_fulltext_search( search_term, max_number_of_results, sid=otobo_sid)
    except APIError as e:
        log.warning( str(e) )
        return json.dumps({"error": str(e)})

    if not raw:
        log.warning( f"Empty search result" )
        return json.dumps({"error": f"Empty search result"})

    return json.dumps(raw)


@server.tool(
    annotations = {
        "title"           : "Do a Ticket fulltext search",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def ticket_fulltext_search( search_term: str, otobo_sid : str = '', max_number_of_results: int = 10  ) -> str:

    """
    Do a fulltext search in OTOBO Zickets for the given search query term.

    Args:
        search_term: the search query term
        destination_queue: Name of the destination queue
        otobo_sid: the OTOBO sessionID
    """
    if not settings.internal_url:
        return json.dumps({"error": "OTOBO_HOST is not configured"})

    try:
        raw = do_ticket_fulltext_search( search_term, max_number_of_results, sid=otobo_sid)
    except APIError as e:
        log.warning( str(e) )
        return json.dumps({"error": str(e)})

    if not raw:
        log.warning( f"Empty search result" )
        return json.dumps({"error": f"Empty search result"})

    return json.dumps(raw)


@server.tool(
    annotations = {
        "title"           : "Find similar tickets",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)
def find_similar_tickets( ticket_id: str, otobo_sid : str = '', article_id : str | None = None ) -> str:

    """
    Find similar tickets to this one.

    Args:
        ticket_id : the ticket id
        article_id : the article id
        otobo_sid: the OTOBO sessionID
    """
    if not settings.internal_url:
        return json.dumps({"error": "OTOBO_HOST is not configured"})

    try:
        raw = do_find_similar_tickets( ticket_id=ticket_id, article_id=article_id, sid=otobo_sid)
    except APIError as e:
        log.warning( str(e) )
        return json.dumps({"error": str(e)})

    if not raw:
        log.warning( f"Empty search result" )
        return json.dumps({"error": f"Empty search result"})

    return json.dumps(raw)


@server.tool(
    annotations = {
        "title"           : "Add a link to another OTOBO Ticket",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    }
)

def link_ticket_to_ticket( ticket_id: str, linked_ticket_id: str, otobo_sid : str = '', dir: str = 'Normal'  ) -> str:

    """
    Link an OTOBO ticket to another OTOBO Ticket

    Args:
        ticket_id : ticket to link from
        linked_ticket_id : ticket to link to
        otobo_sid: the OTOBO sessionID
        dir : link type, default to 'Normal'
    """
    if not settings.internal_url:
        return json.dumps({"error": "OTOBO_HOST is not configured"})

    try:
        raw = do_link_ticket( type='Ticket', ticket_id=ticket_id, linked_ticket_id=linked_ticket_id, linked_faq_id=None, sid=otobo_sid, dir=dir)
    except APIError as e:
        log.warning( str(e) )
        return json.dumps({"error": str(e)})

    if not raw:
        log.warning( f"Empty search result" )
        return json.dumps({"error": f"Empty search result"})

    return json.dumps(raw)


@server.tool(
    annotations = {
        "title"           : "remove a link to another OTOBO Ticket",
        "readOnlyHint"    : False,
        "idempotentHint"  : True,
        "destructiveHint" : True,
        "openWorldHint"   : False,
    }
)

def unlink_ticket_from_ticket( ticket_id: str, linked_ticket_id: str, otobo_sid : str = '', dir: str = 'Normal'  ) -> str:

    """
    Delete a link to another OTOBO Ticket or FAQ

    Args:
        ticket_id : ticket to link from
        linked_ticket_id : ticket id to link to
        linked_faq_id : faq id to link to
        otobo_sid: the OTOBO sessionID
        dir : link type, default to 'Normal'
    """
    if not settings.internal_url:
        return json.dumps({"error": "OTOBO_HOST is not configured"})

    try:
        raw = do_unlink_ticket( type='Ticket', ticket_id=ticket_id, linked_ticket_id=linked_ticket_id, linked_faq_id=None, sid=otobo_sid, dir=dir)
    except APIError as e:
        log.warning( str(e) )
        return json.dumps({"error": str(e)})

    if not raw:
        log.warning( f"Empty search result" )
        return json.dumps({"error": f"Empty search result"})

    return json.dumps(raw)



@server.tool(
    annotations = {
        "title"           : "Get a direct link for a ticket in OTOBO",
        "readOnlyHint"    : True,
        "idempotentHint"  : True,
        "destructiveHint" : False,
        "openWorldHint"   : False,
    })
def get_link_to_ticket(ticket_id: int) -> str:
    """
    Get a valid HTTP link to browse to a specific ticket_id in OTOBO.

    Args:
        ticket_id: Numeric OTOBO ticket ID.
    """

    return json.dumps(settings.ticket_url(ticket_id))


@server.tool(
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

    return json.dumps(settings.faq_url(faq_id))



# main entry point
def main():

    log.info("OTOBO MCP server starting up: transport=%s host=%s port=%s", settings.transport, settings.bind, settings.port)

    if settings.transport == "stdio":
        server.run(transport="stdio")
    else:
        import uvicorn

        if settings.transport == "sse":
            app = server.sse_app()
        else:
            app = server.streamable_http_app()
        uvicorn.run(app, host = settings.bind, port = settings.port)


if __name__ == "__main__":
    main()
