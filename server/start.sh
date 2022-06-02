#!/bin/bash
if [ "$EULA" = "TRUE" ]
then
	sed -i 's/false/TRUE/' eula.txt
fi
java -Xms1G -Xmx3G -jar paper-1.16.5-658.jar nogui
