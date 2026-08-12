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
    OTOBO_MCP_ENABLED_TOOLS        comma separated list of tools to enable
    OTOBO_MCP_ISSUER_URL           OIDC compatible OAuth2 authorizationserver issuer url, eg =https://keycloak:8443/realms/master
    OTOBO_MCP_RESOURCE_SERVER_URL  url to self, eg http://mcp:8765/mcp
    OTOBO_MCP_SCOPES               space separated list of oauth2 scopes, eg 'email' (default)

"""

import importlib


import otobo
import rest

# dynamically import the tools enabled in ENV
# this will load either the oauth2 tools,
# or the plain OTOBO_SESSIONID based tools

tools_prefix = "oauth_tools." if otobo.settings.use_oauth2 else "tools."

for tool in otobo.settings.enabled_tools:

    importlib.import_module( tools_prefix + tool)


if __name__ == "__main__":
    otobo.main()
