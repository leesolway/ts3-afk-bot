"""
main.py: This module serves as the entry point for the TeamSpeak AFK Bot.

It initializes the bot with the necessary configurations and starts its operations on the
TeamSpeak server.
"""

import logging

from bot.core import TeamSpeakAFKBot
from config import settings


def main():
    """
    Entry point of the program.
    Initializes and runs the TeamSpeak AFK Bot.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    afk_bot = TeamSpeakAFKBot(
        server=settings.TS3_SERVER,
        port=settings.QUERY_PORT,
        username=settings.QUERY_USERNAME,
        password=settings.QUERY_PASSWORD,
        server_id=settings.SERVER_ID,
        afk_channel_id=settings.AFK_CHANNEL_ID,
        max_idle_time=settings.MAX_IDLE_TIME,
        mode=settings.MODE,
        channel_ids=settings.CHANNEL_IDS,
    )

    afk_bot.run()


if __name__ == "__main__":
    main()
