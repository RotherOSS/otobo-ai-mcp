# OTOBO AI MCP server

This is the OTOBO MCP server.
It exposes parts of the OTOBO webservices to an LLM as part of the [otobo-ai-services](https://github.com/rotheross/otobo-ai-services).
It assumes a running OTOBO instance with otobo-ai package installed.

## Build

To build the server

```sh
docker compose build
```

To build the `.venv` (only needed if you want to run the integration test client `client.py`)

```sh
# install python uv (here:ubuntu), or use pip
sudo snap install astral-uv --classic

uv venv
source .venv/bin/activate
uv sync

```

## Run MCP Server

```sh
docker compose up -d
```

## Integration Test

The integration test is implemented in the `client.py`.

The MCP uses a OTOBO SessionID bound to the MCP server IP address.
Obtain a session ID:

```sh
docker exec ti mcp curl -vk \
  http://web:5000/otobo/nph-genericinterface.pl/Webservice/Session/Session \
  --header "Content-Type: application/json" \
  --data '{"UserLogin" : "root@localhost", "Password" : "root"}'
```

Run the client with this session id:

```sh
uv run client.py <SessionID>
```

