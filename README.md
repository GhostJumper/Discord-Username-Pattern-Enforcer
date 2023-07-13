# 💬 Discord Username Pattern Enforcer

<img src="https://raw.githubusercontent.com/GhostJumper/Discord-Username-Pattern-Enforcer/main/README/images/icon.png" width=20%>

## 💡 Purpose

This application 💻 enables automatic renaming of users in a Discord server 📡, if their username 🧑 does not conform to the established server pattern, thereby eliminating the manual process of renaming each user individually.

## 🤝 Collaboration

- Use the provided devcontainer 📦 to ensure consistency in development environments.
- Copy `.vscode/example.env` to `.vscode/.env` to configure your environment 🔧.

## 🚀 Execution

### Build the Image yourself:
`docker build -t discord-username-pattern-enforcer:1 .`

### Run the Container:
```
docker run \
    -d \
    --name discord-username-pattern-enforcer \
    -e NAME_PATTERN=^.+\/\/.+$ \
    -e DEFAULT_DISPLAY_NAME=Default//Name \
    -e DISCORD_SERVER_ID=Your_Server_ID \
    -e DISCORD_BOT_TOKEN=Your_Token \
    -e DRY_RUN=true \
    -e ALLOW_BOT_RENAMING=false \
    -e LOG_LEVEL=INFO \
    unrea1/discord-username-pattern-enforcer:4
```
⚠️ **Note:** This application will not rename any users unless `DRY_RUN` is set to `false`. ⚠️