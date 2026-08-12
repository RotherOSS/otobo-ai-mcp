
import os
import sys
import jwt
import json
import logging
import requests
import argparse

from pydantic import AnyHttpUrl

from typing import Any
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from mcp.server.auth.provider import AccessToken, TokenVerifier#, AccessTokenT
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions


default_tools_enabled = ",".join([
    "faq_fulltext_search",
    "get_link_to_faq",
    "get_ticket_details",
    "ticket_fulltext_search",
    "unlink_ticket_to_ticket",
    "find_similar_tickets",
    "get_link_to_ticket",
    "link_ticket_to_ticket",
    "transfer_ticket_to_destination_queue",
    "update_generated_response"
])


# Configuration
class Settings:

    def __init__(self):
        self.bind          = os.environ.get("OTOBO_MCP_BIND", "0.0.0.0")
        self.port          = int(os.environ.get("OTOBO_MCP_PORT", 8765))
        self.internal_url  = os.environ.get("OTOBO_MCP_INTERNAL_URL", "http://web:5000/").rstrip("/")
        self.public_url    = os.environ.get("OTOBO_MCP_PUBLIC_URL", "https://localhost/otobo/index.pl")
        self.webservice    = os.environ.get("OTOBO_MCP_WEBSERVICE", "OTOBO-AI")
        self.ssl_verify    = os.environ.get("OTOBO_MCP_SSL_VERIFY", "false").lower() in ("true", "1", "yes")
        self.timeout       = int(os.environ.get("OTOBO_MCP_TIMEOUT", 30))
        self.transport     = os.environ.get("OTOBO_MCP_TRANSPORT", "streamable-http")
        self.loglevel      = int(os.environ.get("OTOBO_MCP_LOGLEVEL",40)) # see https://docs.python.org/3/library/logging.html#logging-levels
        self.enabled_tools = os.environ.get("OTOBO_MCP_ENABLED_TOOLS",default_tools_enabled).split(",") 
        # oauth2 only
        self.use_oauth2          = os.environ.get("OTOBO_MCP_OAUTH","false").lower() in ("true", "1", "yes")
        self.issuer_url          = AnyHttpUrl( os.environ.get("OTOBO_MCP_ISSUER_URL", "https://keycloak:8443/realms/master") )
        self.resource_server_url = AnyHttpUrl( os.environ.get("OTOBO_MCP_RESOURCE_SERVER_URL", "http://mcp:8765/mcp") )
        self.required_scopes     = os.environ.get("OTOBO_MCP_SCOPES", "email").split(" ")


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

# Extract the OAuth2 Token so the framework is happy and we
# can forward it to OTOBO for actual validation

class PassthroughTokenVerifier(TokenVerifier):

    async def verify_token(self, token: str) -> AccessToken | None:

        log.info(f"TOKEN {token}")

        t = jwt.decode( token, options={"verify_signature": False})
        log.info(f"{t}")

        return AccessToken(
            token=token,
            client_id=t.get("azp"),
            scopes=t.get("scope").split(" "),
            expires_at=t.get("exp"),
            subject=t.get("sub"),
            claims=t
        )


# server instance 
server = None

if settings.use_oauth2:

    server = FastMCP(
        "otobo-mcp-server",
        transport_security = TransportSecuritySettings(
            enable_dns_rebinding_protection = False,
        ),
        json_response  = True,
        token_verifier = PassthroughTokenVerifier(),
        auth           = AuthSettings(
            issuer_url                  = settings.issuer_url,
            resource_server_url         = settings.resource_server_url,
            required_scopes             = settings.required_scopes,
            client_registration_options = ClientRegistrationOptions(
                enabled = False,
            ),
        )
    )


else:
    server = FastMCP(
        "otobo-mcp-server",
        transport_security = TransportSecuritySettings(
            enable_dns_rebinding_protection = False,
        )
    )



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

    return out


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
