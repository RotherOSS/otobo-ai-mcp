import asyncio
import os
import sys

from pydantic import AnyUrl

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.context import RequestContext


async def handle_log(params: types.LoggingMessageNotificationParams) -> None:
    """Handle log messages from the server."""
    print(f"[{params.level}] {params.data}")



async def run(SessionID):

    print("run\n");

    async with streamable_http_client("http://localhost:8765/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        print("connect\n");

        async with ClientSession(read_stream, write_stream, logging_callback=handle_log) as session:

            print("init\n");
            # Initialize the connection
            await session.initialize()

            # List available prompts
            prompts = await session.list_prompts()
            print(f"Available prompts: {[p.name for p in prompts.prompts]}")

            # List available resources
            resources = await session.list_resources()
            print(f"Available resources: {[r.uri for r in resources.resources]}")

            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call a tool (add tool from fastmcp_quickstart)
            result = await session.call_tool("get_ticket_details", arguments={"ticket_id": 2, "include_articles": True, "otobo_sid" : SessionID })
            result_unstructured = result.content[0]
            if isinstance(result_unstructured, types.TextContent):
                print(f"Tool result: {result_unstructured.text}")
            result_structured = result.structuredContent
            print(f"Structured tool result: {result_structured}")

            # Call a tool (add tool from fastmcp_quickstart)
#            result = await session.call_tool("get_link_to_ticket", arguments={"ticket_id": 1} )
#            result_unstructured = result.content[0]
#            if isinstance(result_unstructured, types.TextContent):
#                print(f"Tool result: {result_unstructured.text}")
#            result_structured = result.structuredContent
#            print(f"Structured tool result: {result_structured}")

            # Call a tool (add tool from fastmcp_quickstart)
#            result = await session.call_tool("update_generated_response", arguments={"ticket_id": 1, "generated_response" : "Holla die Waldfee!", "otobo_sid" : SessionID } ) #, "article_id" : 20 } )
#            result_unstructured = result.content[0]
#            if isinstance(result_unstructured, types.TextContent):
#                print(f"Tool result: {result_unstructured.text}")
#            result_structured = result.structuredContent
#            print(f"Structured tool result: {result_structured}")

            # Call a tool (add tool from fastmcp_quickstart)
#            result = await session.call_tool("transfer_ticket_to_destination_queue", arguments={"ticket_id": 1, "destination_queue" : "Test", "otobo_sid" : SessionID } )
#            result_unstructured = result.content[0]
#            if isinstance(result_unstructured, types.TextContent):
#                print(f"Tool result: {result_unstructured.text}")
#            result_structured = result.structuredContent
 #           print(f"Structured tool result: {result_structured}")

            # Call a tool (add tool from fastmcp_quickstart)
#            result = await session.call_tool("faq_fulltext_search", arguments={"search_term": "Katze", "otobo_sid" : SessionID } )
#            result_unstructured = result.content[0]
#            if isinstance(result_unstructured, types.TextContent):
#                print(f"Tool result: {result_unstructured.text}")
#            result_structured = result.structuredContent
#            print(f"Structured tool result: {result_structured}")

            # Call a tool (add tool from fastmcp_quickstart)
            result = await session.call_tool("link_ticket_to_ticket", arguments={"ticket_id": "1", "linked_ticket_id" : "2", "otobo_sid" : SessionID } )
            result_unstructured = result.content[0]
            if isinstance(result_unstructured, types.TextContent):
                print(f"Tool result: {result_unstructured.text}")
            result_structured = result.structuredContent
            print(f"Structured tool result: {result_structured}")

            result = await session.call_tool("unlink_ticket_from_ticket", arguments={"ticket_id": "1", "linked_ticket_id" : "2", "otobo_sid" : SessionID } )
            result_unstructured = result.content[0]
            if isinstance(result_unstructured, types.TextContent):
                print(f"Tool result: {result_unstructured.text}")
            result_structured = result.structuredContent
            print(f"Structured tool result: {result_structured}")

            result = await session.call_tool("find_similar_tickets", arguments={"ticket_id": "2", "otobo_sid" : SessionID } )
            result_unstructured = result.content[0]
            if isinstance(result_unstructured, types.TextContent):
                print(f"Tool result: {result_unstructured.text}")
            result_structured = result.structuredContent
            print(f"Structured tool result: {result_structured}")


def main():
    """Entry point for the client script."""
    SessionID = str(sys.argv[1]) if len(sys.argv) > 1 else ""
    asyncio.run(run(SessionID))


if __name__ == "__main__":
    main()

