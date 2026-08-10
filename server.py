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
"""

import importlib


import otobo
import rest

# dynamically import the tools enabled in ENV
for tool in otobo.settings.enabled_tools:

    importlib.import_module("tools." + tool)


if __name__ == "__main__":
    otobo.main()
