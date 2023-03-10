# Template 1.19 Minecraft Server

This is an automated repository that automatically uploads a **template 1.19 minecraft server** to the GitHub Container Registry.
It it hosted at `ghcr.io/portalhubyt/template_server:latest`. Anytime there are modifications made to the server folder of the repository, the image will be updated and uploaded to reflect the changes.

# Usage:
- Fetch the image
```
docker pull ghcr.io/portalhubyt/template_server:latest
```

- Run the image
```
docker run -d --pull=always -e EULA=TRUE -p 25575:25575 -p 25565:25565 ghcr.io/portalhubyt/template_server:latest 
```

Mandatory options:
- `-e EULTA=TRUE` Needed to accept Spigot's EULA before launching.
- `-p 555:25565` Port redirection, left is on host, right is in container. That means we make the server available on host's 555 port.
- `--network host` **If you don't use -p**, it'll use host's network interfaces.

Additional options:
- `-d` Run in detach mode (background).
- `--pull=always` This is will always attempt to update the local image, will do nothing if you're up-to-date.

# Plugins:
| Name + Link        | Description           |
| ------------- |:-------------:| 
| [`Citizens`](https://www.spigotmc.org/resources/citizens.13811/)      | NPCs creator & manager |
| [`Denizen`](https://www.spigotmc.org/resources/denizen.21039/)      | Complements [`Citizens`](https://www.spigotmc.org/resources/citizens.13811/), allows for scripting NPCs |
| [`Sentinel`](https://www.spigotmc.org/resources/sentinel.22017/)      | Complements [`Citizens`](https://www.spigotmc.org/resources/citizens.13811/), allows for NPCs to fight |
| [`FAWE`](https://www.spigotmc.org/resources/fastasyncworldedit.13932/)      | Fast and Asynchronous World Edit version |
| [`LibsDisguises`](https://www.spigotmc.org/resources/libs-disguises-free.81/)      | Disguise any entity into any other entity |
| [`Multiverse-Core`](https://www.spigotmc.org/resources/multiverse-core.390/)      | World creator & manager |
| [`Sudo`](https://www.spigotmc.org/resources/sudo.13730/)      | Execute arbitrary commands from another player |
| [`VoidGen`](https://www.spigotmc.org/resources/voidgen.25391/)      | Create completely empty worlds from [`Multiverse-Core`](https://www.spigotmc.org/resources/multiverse-core.390/) |
| [`WorldGuard`](https://dev.bukkit.org/projects/worldguard)      | Put restrictions into specific part of the map |
