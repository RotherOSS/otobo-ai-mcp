# OTOBO AI MCP Server

This is the OTOBO MCP server.
It exposes parts of the OTOBO webservices to an LLM as part of the [otobo-ai-services](https://github.com/rotheross/otobo-ai-services).

> [!IMPORTANT]
> It assumes a running OTOBO instance with otobo-ai package installed.

## Available MCP Tools

| Tool                               | Description                                         |
|------------------------------------|-----------------------------------------------------|
|ticket_fulltext_search              | does a fulltext search in ES for tickets            |
|faq_fulltext_search                 | does a fulltext search in ES for FAQs               |
|get_ticket_details                  | retrieve ticket detail data including articles and links |
|transfer_ticket_to_destination_queue| move ticket to another queue                        |
|update_generated_response           | update the AI generated response for an article of a ticket in OTOBO |
|find_similar_tickets                | find similar tickets in vector DB                   |
|link_ticket_to_ticket               | link a ticket to another ticket in OTOBO            |
|unlink_ticket_from_ticket           | remove a link from a ticket to another ticket       |
|get_link_to_ticket                  | retrieve URL that links to a ticket in OTOBO        |
|get_link_to_faq                     | retrieve URL that links to a FAQ item in OTOBO      |

All tools - except for the last two link generation tools - need a valid
OTOBO SessionID (sid).
When the chat is invoked from OTOBO,
this sid will be passed.

> [!NOTE]
> This sid will be bound to the AI chat and is not usable in another context.

## Fenced Output

Every tool result and tool error message is wrapped in a fence to keep prompt injection from OTOBO data at bay:

```
<<<OTOBO_DATA_BEGIN 3f9c…>>>
{"ticket_id": 1, …}
<<<OTOBO_DATA_END 3f9c…>>>
```

The nonce is generated anew for each tool call, so a ticket cannot guess the closing fence.
The server instructions explain the fence to the LLM and tell it to treat the fenced content as data, never as instructions.

Configure the fence with `OTOBO_MCP_FENCE_PREFIX` and `OTOBO_MCP_FENCE_SUFFIX`.

> [!NOTE]
> Tools registered with `@otobo.tool(...)` are fenced.
> Do not register tools with `@otobo.server.tool(...)`, as their output stays unfenced.

> [!IMPORTANT]
> Both must contain the placeholder `{nonce}` and must differ from each other, otherwise the server refuses to start.

## Build

To build the server

```sh
docker compose build
```

## Run MCP Server

```sh
docker compose up -d
```

## Integration Test

The integration test is implemented in the `client.py`.

```sh
cd it
```

### One Time Preparation

> [!TIP]
> Building the `.venv` is needed only once.

1) install python `uv` if not available yet

```sh
# install python uv (here:ubuntu), or use pip
sudo snap install astral-uv --classic
uv venv
source .venv/bin/activate
uv sync
```

### Init Virtual Env

After the initial run,
you can re-activate the virtual env for the current terminal:

```sh
source .venv/bin/activate
```

### Obtain OTOBO Session ID (sid)

> [!NOTE]
> The MCP uses an OTOBO SessionID bound to the MCP server IP address.

For testing, obtain a session ID like so:

```sh
docker exec -ti mcp curl -vk \
  http://web:5000/otobo/nph-genericinterface.pl/Webservice/Session/Session \
  --header "Content-Type: application/json" \
  --data '{"UserLogin" : "root@localhost", "Password" : "root"}'
```

### Run Integration Test

Run the client with the session id from above:

```sh
uv run client.py <SessionID>
```

