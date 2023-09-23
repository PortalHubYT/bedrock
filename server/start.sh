#!/bin/bash

if [ "$EULA" = "TRUE" ]; then
    sed -i 's/false/TRUE/' eula.txt
fi

# Find the JAR file using a wildcard
JAR_FILE=$(ls paper-*.jar | head -n 1)

if [ -z "$JAR_FILE" ]; then
    echo "Error: No paper JAR file found"
    exit 1
fi

java -Xms1G -Xmx4G -jar $JAR_FILE nogui