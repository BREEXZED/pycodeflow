FROM ubuntu:24.04 

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    curl wget git unzip jq \
    python3 python3-pip python3-venv \ 
    nodejs npm \
    build-essential \
    ripgrep fd-find \
     nano vim \
 && rm -rf /var/lib/aptI/lists/*

WORKDIR /workspace
