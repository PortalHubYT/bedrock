# https://github.com/itzg/docker-minecraft-server
FROM itzg/minecraft-server:latest

# Install Python
RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install requests

# Copy and run the plugin fetching script
COPY fetch_plugins.py /tmp/fetch_plugins.py
RUN python3 /tmp/fetch_plugins.py

COPY profile.yml /tmp/profile.yml
COPY parse.py /tmp/parse.py
RUN python3 /tmp/parse.py /tmp/profile.yml

# Copy the .env file
COPY /tmp/.env .env

# Placeholder CMD (replace with your actual application)
CMD ["/start"]