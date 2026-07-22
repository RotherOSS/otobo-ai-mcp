# OTOBO AI MCP server

assumes a running OTOBO instance with otobo-ai package installed.

# build

to build the server

```
docker compose build
``` 

to build the .venv (only needed if you want to run the integration test
client client.py)

```
# install python uv (here:ubuntu), or use pip
sudo snap install astral-uv --classic

uv venv
source .venv/bin/activate
uv sync

```

# run MCP server

```
docker compose up -d
```

## integration test (client.py)

### OTOBO SessionID

The MCP uses a OTOBO SessionID bound to the MCP server ip address.
Create one using:

```
# first open a shell inside the mcp docker containwe
docker exec -ti mcp bash
# inside the mcp, run curl
curl -vk http://web:5000/otobo/nph-genericinterface.pl/Webservice/Session/Session -H"Content-Type: application/json" --data '{"UserLogin" : "root@localhost", "Password" : "root"}'
```


### run the integration test client
```
uv run client.py <SessionID>
``` 

