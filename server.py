#!/usr/bin/env python3
"""
OTOBO AI MCP Server — interact with OTOBO REST API via MCP

Environment:
    OTOBO_MCP_BIND                 Bind address, default is 0.0.0.0
    OTOBO_MCP_PORT                 MCP server port, default is 8765
    OTOBO_MCP_INTERNAL_URL         Webservice endpoint eg http://web:5000/ when running under Docker
    OTOBO_MCP_PUBLIC_URL           Public base url, eg to point the user's browser to
    OTOBO_MCP_WEBSERVICE           Web service name (default: OTOBO-AI)
    OTOBO_MCP_SSL_VERIFY           SSL verification (default: true)
    OTOBO_MCP_TIMEOUT              HTTP timeout in seconds (default: 30)
    OTOBO_MCP_TRANSPORT            Transport: stdio, sse, streamable-http (default: streamable-http)
    OTOBO_MCP_LOGLEVEL             log level as number or name (default: 20 = INFO):
                                   50 = CRITICAL, 40 = ERROR, 30 = WARNING, 20 = INFO, 10 = DEBUG, 0 = NOTSET (all)
    OTOBO_MCP_ENABLED_TOOLS        comma separated list of tools to enable (default: all)
    OTOBO_MCP_FENCE_PREFIX         line before each tool result, must contain {nonce} (default: <<<OTOBO_DATA_BEGIN {nonce}>>>)
    OTOBO_MCP_FENCE_SUFFIX         line after each tool result, must contain {nonce} (default: <<<OTOBO_DATA_END {nonce}>>>)
    OTOBO_MCP_MAX_TOKENS           token limit of a read-only tool result, longer results are chunked (default: 10000)
    OTOBO_MCP_CHARS_PER_TOKEN      characters per token to estimate the token count (default: 3)
    OTOBO_MCP_IGNORED_LINKED_TICKET_STATES  comma separated states of linked tickets left out (default: merged,removed)
    OTOBO_MCP_STATELESS            run streamable-http without MCP sessions, eg for several workers (default: false)
    OTOBO_MCP_ELICITATION          user confirmation of write tools: required, advised or none (default: required)
    OTOBO_MCP_ELICITATION_TIMEOUT  seconds to wait for the user's confirmation (default: 300)
    OTOBO_MCP_OAUTH                use OAuth2 bearer tokens instead of OTOBO session IDs (default: false)
    OTOBO_MCP_ISSUER_URL           OIDC compatible OAuth2 authorization server issuer url, eg https://keycloak:8443/realms/master
    OTOBO_MCP_RESOURCE_SERVER_URL  url to self, eg http://mcp:8765/mcp
    OTOBO_MCP_SCOPES               space separated list of oauth2 scopes, eg 'email' (default)

"""

import importlib

import otobo

# dynamically import the tools enabled in ENV
# this will load either the oauth2 tools,
# or the plain OTOBO_SESSIONID based tools

tools_prefix = "oauth_tools." if otobo.settings.use_oauth2 else "tools."

otobo.log.info("enabled tools: %s", ", ".join(otobo.settings.enabled_tools))

for tool in otobo.settings.enabled_tools:

    importlib.import_module(tools_prefix + tool)


if __name__ == "__main__":
    otobo.main()
