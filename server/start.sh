#!/bin/bash
if [ "$EULA" = "TRUE" ]
then
	sed -i 's/false/TRUE/' eula.txt
fi
java -Xms1G -Xmx4G -jar paper-1.19.4-550.jar nogui
