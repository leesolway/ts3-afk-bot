import logging

from bot.core import TeamSpeakAFKBot
import config.settings as settings


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    afk_bot = TeamSpeakAFKBot(
        server=settings.TS3_SERVER,
        port=settings.QUERY_PORT,
        username=settings.QUERY_USERNAME,
        password=settings.QUERY_PASSWORD,
        server_id=settings.SERVER_ID,
        afk_channel_id=settings.AFK_CHANNEL_ID,
        max_idle_time=settings.MAX_IDLE_TIME,
        blacklist_channel_ids=settings.BLACKLIST_CHANNEL_IDS,
        whitelist_channel_ids=settings.WHITELIST_CHANNEL_IDS
    )

    afk_bot.run()

if __name__ == "__main__":
    main()
