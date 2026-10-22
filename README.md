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

## Chunked Output

Tickets may be arbitrarily long, while the context of the LLM is limited.
Every read-only tool accepts the parameter `max_tokens`, defaulting to `OTOBO_MCP_MAX_TOKENS`.
A longer result is split into chunks.
The first chunk is returned, followed by a hint how to retrieve the next one:

```
Chunk 1 of 4. Repeat the call with chunk=2 and result_hash="1a2b3c4d".
```

Pagination is stateless, each chunk is a new call fetching the data from OTOBO again.
If the data changed in between, the `result_hash` no longer matches and the LLM is asked to start again with chunk 1.

> [!NOTE]
> The token count is estimated from the length of the result using `OTOBO_MCP_CHARS_PER_TOKEN`, as the tokenizer of the LLM is unknown to the server.

> [!NOTE]
> Write tools are not chunked, as repeating their call would repeat the change.

## Confirmation of Write Tools

Before a write tool changes OTOBO data,
the user is asked to confirm the action via [MCP elicitation](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation),
eg:

```
Move ticket 4711 to queue 'IT'?
```

So a prompt injection cannot make the LLM change data unnoticed.
The tool fails if the user declines, cancels or does not respond within `OTOBO_MCP_ELICITATION_TIMEOUT` seconds.

`OTOBO_MCP_ELICITATION` decides whether the confirmation is

| value      | behaviour                                                             |
|------------|-----------------------------------------------------------------------|
| `required` | requested, write tools fail if the client does not support elicitation |
| `advised`  | requested only if the client supports elicitation                     |
| `none`     | never requested, eg for an AI agent acting without a user             |

The default is `required`.

> [!NOTE]
> Write tools, ie with `readOnlyHint` false, must pass a `confirmation` message to `@otobo.tool(...)`.
> It is a template filled with the arguments of the call, eg `"Move ticket {ticket_id} to queue '{destination_queue}'?"`.

> [!IMPORTANT]
> With `OTOBO_MCP_STATELESS` the server does not know the client capabilities,
> so `required` lets all write tools fail and `advised` never asks.

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

