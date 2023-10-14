# https://github.com/itzg/docker-minecraft-server
# Base image
FROM itzg/minecraft-server:latest

# Install Python
RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN pip install requests pyyaml

# Copy necessary files
COPY prepare.py /tmp/prepare.py
COPY profile.yml /tmp/profile.yml

# Accept the IMG_TAG as a prepare argument
ARG IMG_TAG=classic
ARG DEBUG=false

# Run the prepare.py script with the provided IMG_TAG
RUN python3 /tmp/prepare.py $IMG_TAG $DEBUG

COPY dockman.sh /tmp/
RUN chmod +x /tmp/dockman.sh

ENTRYPOINT [ "/tmp/dockman.sh", "--entrypoint" ]