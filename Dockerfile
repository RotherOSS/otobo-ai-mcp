# Base image with Python
FROM python:3.12-slim

# Install build tools and useful Debian packages
RUN apt-get update \
    && apt-get -y --no-install-recommends install \
    tree \
    vim \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

# Copy requirements and install
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/toon-format/toon-python.git

# Copy source code
COPY ./server.py /server.py

# RUN
ENTRYPOINT [ "python", "/server.py" ]

