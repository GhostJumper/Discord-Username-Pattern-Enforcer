# 💬 Discord Username Pattern Enforcer

## 💡 Purpose

This application 💻 enables automatic renaming of users in a Discord server 📡, if their username 🧑 does not conform to the established server pattern, thereby eliminating the manual process of renaming each user individually.

## 🤝 Collaboration Guidelines

- Use the provided devcontainer 📦 to ensure consistency in development environments.
- Copy `.vscode/example.env` to `.vscode/.env` to configure your environment 🔧.

## 🚀 Execution

### Build the Image:
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
    unrea1/discord-username-pattern-enforcer:2
```
⚠️ **Note:** This application will not rename any users unless `DRY_RUN` is set to `false`. ⚠️