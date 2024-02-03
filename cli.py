import logging
import argparse

from bot.ts3_api import TS3API
import config.settings as settings

def list_channels(ts3_api):
    try:
        channels = ts3_api.list_channels()
        if channels:
            print("List of Channels:")
            for channel in channels:
                print(f"- {channel['channel_name']} (ID: {channel['cid']})")
        else:
            print("No channels found on the server.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='TeamSpeak AFK Bot CLI')
    parser.add_argument('--list-channels', action='store_true', help='List channels on the TeamSpeak server')

    args = parser.parse_args()

    ts3_api = TS3API(
        server=settings.TS3_SERVER,
        query_port=settings.QUERY_PORT,
        username=settings.QUERY_USERNAME,
        password=settings.QUERY_PASSWORD
    )

    if args.list_channels:
        ts3_api.connect()
        ts3_api.use(server_id=settings.SERVER_ID)
        list_channels(ts3_api)
        ts3_api.disconnect()


if __name__ == "__main__":
    main()
