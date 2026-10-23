# Base image with Python
FROM python:3.12-slim

# curl is used to obtain an OTOBO session ID for testing, see README
RUN apt-get update \
    && apt-get -y --no-install-recommends install \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

# Copy requirements and install
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
RUN mkdir /mcp
COPY ./server.py /mcp/server.py
COPY ./otobo.py /mcp/otobo.py
COPY ./rest.py /mcp/rest.py
COPY ./domain /mcp/domain
COPY ./tools /mcp/tools
COPY ./oauth_tools /mcp/oauth_tools

RUN useradd --system --no-create-home mcp
USER mcp

# RUN
ENTRYPOINT [ "python", "/mcp/server.py" ]

