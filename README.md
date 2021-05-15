# template_server


This repo hosts the presets and sources needed to build a Docker image runnng minecraft spiggot (1.16 atm) then upload it to github container registry.


# Usage:
- Fetch the image
```
docker pull ghcr.io/portalhubyt/template_server:latest
```

- Run the image
```
docker run -d -e EULA=TRUE -p 555:25565 ghcr.io/portalhubyt/template_server:latest 
```

Mandatory options:
-e EULTA=TRUE : Needed to accept spiggot's EULA before launching.
-p 555:25565 : port redirection, left is on host, right is in container. That means we make the server available on host's 555 port.
OR 
--network host to use host's network interfaces

Additional options:
-d : run in detach mode (background)
