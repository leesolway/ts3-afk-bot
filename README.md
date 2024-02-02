# TeamSpeak 3 AFK Bot

## Introduction
TeamSpeak 3 AFK Bot is a simple, lightweight bot designed to manage user presence on a TeamSpeak 3 server. It automatically moves users who have been idle for a specified amount of time to an AFK (Away From Keyboard) channel.

## Features
- Monitors user idle times on a TeamSpeak 3 server.
- Moves users who have been idle for too long to a designated AFK channel.
- Configurable idle time and AFK channel through environment variables.
- Dockerized for easy deployment and isolation.

## Requirements
- Docker
- A TeamSpeak 3 server with ServerQuery access

## Installation and Usage

### Building the Docker Image
1. Clone the repository:
    ```bash
    git clone https://github.com/leesolway/ts3-afk-bot.git
    cd ts3-afk-bot
    ```
2. Build the Docker image:
    ```bash
    docker build -t leesolway/ts3-afk-bot .
    ```

### Running the Bot
Run the Docker container, replacing the environment variable values with your actual TeamSpeak server details:
```bash
docker run -d \
  -e TS3_SERVER=your_teamspeak_server_ip \
  -e QUERY_PORT=your_query_port \
  -e SERVER_ID=your_server_id \
  -e QUERY_USERNAME=your_query_username \
  -e QUERY_PASSWORD=your_query_password \
  -e AFK_CHANNEL_ID=your_afk_channel_id \
  -e MAX_IDLE_TIME=your_max_idle_time \
  leesolway/ts3-afk-bot:latest


## Using Docker Compose

### 1. Create a `docker-compose.yml` File

```yaml
version: '3.8'
services:
  ts3-afk-bot:
    image: leesolway/ts3-afk-bot:latest
    environment:
      TS3_SERVER: your_teamspeak_server_ip
      QUERY_PORT: your_query_port
      SERVER_ID: your_server_id
      QUERY_USERNAME: your_query_username
      QUERY_PASSWORD: your_query_password
      AFK_CHANNEL_ID: your_afk_channel_id
      MAX_IDLE_TIME: your_max_idle_time
    restart: unless-stopped
```

## Environment Variables

| Variable        | Description                                          | Default Value |
|-----------------|------------------------------------------------------|---------------|
| `TS3_SERVER`    | The IP address of your TeamSpeak 3 server.           | None          |
| `QUERY_PORT`    | The ServerQuery port of your TeamSpeak 3 server.     | `10011`       |
| `SERVER_ID`     | The virtual server ID.                               | `1`           |
| `QUERY_USERNAME`| The ServerQuery username.                            | None          |
| `QUERY_PASSWORD`| The ServerQuery password.                            | None          |
| `AFK_CHANNEL_ID`| The channel ID where idle users will be moved.       | None          |
| `MAX_IDLE_TIME` | The maximum idle time (in milliseconds) before a user is considered AFK. | None  |