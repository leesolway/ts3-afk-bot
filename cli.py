import logging
import argparse

from bot.core import TeamSpeakAFKBot
from bot.ts3_api import TS3API
import config.settings as settings


def list_channels(ts3_api):
    ts3_api.connect()
    ts3_api.use(server_id=settings.SERVER_ID)

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
    finally:
        ts3_api.disconnect()


def list_idle_users(ts3_api, channel_ids, mode):
    ts3_api.connect()
    ts3_api.use(server_id=settings.SERVER_ID)

    try:
        # Get all channels and users on the server
        clients = ts3_api.get_clients()
        channels = ts3_api.list_channels()

        if not clients:
            print("No clients found on the server.")
            return

        # Filter channels based on mode and channel_ids
        filtered_channels = [
            channel for channel in channels if TeamSpeakAFKBot.should_process_channel(channel['cid'], settings.AFK_CHANNEL_ID, mode, channel_ids)
        ]

        for channel in filtered_channels:
            clients_in_channel = [client for client in clients if client['cid'] == channel['cid']]

            if clients_in_channel:
                print(f"Users in channel {channel['channel_name']} (ID: {channel['cid']}):")
                for client in clients_in_channel:
                    idle_time = client.get('client_idle_time', 'Unknown')
                    print(f"- {client['client_nickname']} (ID: {client['clid']}) - Idle time: {idle_time}")
            else:
                print(f"No users found in channel {channel['channel_name']} (ID: {channel['cid']}).")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ts3_api.disconnect()


def main():
    parser = argparse.ArgumentParser(description='TeamSpeak AFK Bot CLI')
    parser.add_argument('--list-channels', action='store_true', help='List channels on the TeamSpeak server')
    parser.add_argument('--list-idle-users', action='store_true', help='List users in the supported channels along with their idle time')

    args = parser.parse_args()

    ts3_api = TS3API(
        server=settings.TS3_SERVER,
        query_port=settings.QUERY_PORT,
        username=settings.QUERY_USERNAME,
        password=settings.QUERY_PASSWORD
    )

    if args.list_channels:
        list_channels(ts3_api)

    if args.list_idle_users:
        list_idle_users(ts3_api, settings.CHANNEL_IDS, settings.MODE)

if __name__ == "__main__":
    main()
