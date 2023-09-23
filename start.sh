docker run --name minecraft_server -d --pull=always -e EULA=TRUE -p 25575:25575 -p 25565:25565 -p 4567:4567 ghcr.io/portalhubyt/template_server:latest
