# Base image with Python
FROM python:3.12-slim

# Install build tools and useful Debian packages
RUN apt-get update \
    && apt-get -y --no-install-recommends install \
    tree \
    vim \
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

# RUN
ENTRYPOINT [ "python", "/mcp/server.py" ]

