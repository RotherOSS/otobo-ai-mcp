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


# globals

settings  = Settings()

# logging

log = logging.getLogger("otobo-mcp")
logging.basicConfig(level=settings.loglevel, format="%(asctime)s %(levelname)s %(name)s: %(message)s", stream=sys.stderr)


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
    log.debug( f"POST url: {url}")
    
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
    if data.get("Error"):
        err = data["Error"]
        raise APIError(f"{err.get('ErrorCode', '?')}: {err.get('ErrorMessage', '?')}")

    log.debug(data)
    return data
    
    
# helpers and filters    

def do_get_ticket(ticket_id: int, all_articles: bool = True, sid: str = "") -> dict:

    data = get_operation(
        "Ticket/" + str(ticket_id), 
        {
            "AllArticles": "1" if all_articles else "0",        
            "DynamicFields": "1",
            "SessionID" : sid,
        }
    )
    tickets = data.get("Ticket", [])
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


def fetch_articles(ticket: dict) -> list[dict]:

    articles = ticket.get("Article", [])
    if isinstance(articles, dict):
        return [articles]
    return articles


def filter_ticket(ticket: dict, include_articles: bool = True) -> dict:

    out = {
        "ticket_id": ticket.get("TicketID"),
        "ticket_number": ticket.get("TicketNumber"),
        "title": ticket.get("Title"),
        "state": ticket.get("State"),
        "priority": ticket.get("Priority"),
        "queue": ticket.get("Queue"),
        "customer": ticket.get("CustomerUserID"),
        "owner": ticket.get("Owner"),
        "created": ticket.get("Created"),
        "changed": ticket.get("Changed"),
        "url": settings.ticket_url(ticket["TicketID"]) if ticket.get("TicketID") else None,
    }

    dynamic = {k.replace("DynamicField_", ""): v
               for k, v in ticket.items() if k.startswith("DynamicField_") and v}
               
    if dynamic:
        out["dynamic_fields"] = dynamic

    if include_articles:
        out["articles"] = [filter_article(a) for a in fetch_articles(ticket)]

    return out


def filter_article(article: dict) -> dict:

    OTOBOAI = None
    DFS = article.get("DynamicField")
    for DF in DFS:
        if ( DF.get("Name","") == "OTOBOAI" ):
            OTOBOAI = DF.get("Value")
            
    return {
        "article_id": article.get("ArticleID"),
        "from": article.get("From"),
        "to": article.get("To"),
        "subject": article.get("Subject"),
        "body": article.get("Body"),
        "created": article.get("CreateTime", article.get("Created")),
        "channel": article.get("CommunicationChannel", article.get("ArticleType")),
        "sender_type": article.get("SenderType"),
        "generated_answer" : OTOBOAI,
    }


# the MCP tools available via this MCP

@server.tool()
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

@server.tool()
def update_generated_response(ticket_id: int, generated_response: str, article_id: int = None, otobo_sid : str = '') -> bool:

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

    return raw['Success'] == 1

@server.tool()
def transfer_ticket_to_destination_queue(ticket_id: int, destination_queue: str, otobo_sid : str = '') -> bool:

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

    return raw['TicketID'] == str(ticket_id)


@server.tool()
def get_link_to_ticket(ticket_id: int) -> str:
    """ 
    Get a valid HTTP link to browse to a specific ticket_id in OTOBO.

    Args:
        ticket_id: Numeric OTOBO ticket ID.
    """

    return json.dumps(settings.ticket_url(ticket_id))



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
