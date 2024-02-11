import logging

from .ts3_api import TS3API

class TeamSpeakAFKBot:
    def __init__(
        self, server, port, username, password, server_id, afk_channel_id, max_idle_time,
        channel_ids, mode
    ):
        self.ts3_api = TS3API(server, port, username, password)
        self.server_id = server_id
        self.afk_channel_id = afk_channel_id
        self.max_idle_time = max_idle_time
        self.channel_ids = channel_ids or []
        self.mode = mode

    @staticmethod
    def should_process_channel(cid, afk_channel_id, mode, channel_ids):
        """
        Determines whether a given channel should be processed based on the bot's mode and channel IDs.

        Parameters:
        cid: The channel to check.

        Returns:
        bool: True if the channel should be processed, False otherwise.
        """

        is_valid_channel = cid is not None
        is_not_afk_channel = cid != afk_channel_id
        is_blacklisted = mode == 'blacklist' and cid in channel_ids
        is_whitelisted = mode == 'whitelist' and cid not in channel_ids

        return is_valid_channel and is_not_afk_channel and (is_blacklisted or is_whitelisted)

    def is_user_afk(self, client_idle_time):
        """
        Check if a user is considered AFK based on idle time.

        :param client_idle_time: The idle time of the client.
        :return: True if the user is considered AFK, False otherwise.
        """
        return int(client_idle_time) > self.max_idle_time

    def move_client_to_afk(self, client_info):
        """
        Move a client to the AFK channel.

        :param client_info: Information about the client to move.
        """
        client_id = client_info['clid']
        client_nickname = client_info.get('client_nickname', 'Unknown')

        try:
            self.ts3_api.move_client(client_id, self.afk_channel_id)
            logging.info(f"Moved client {client_nickname} (ID: {client_id}) to AFK channel.")
        except Exception as e:
            logging.error(f"An error occurred while moving client {client_nickname} (ID: {client_id}) to AFK channel: {e}")

    def should_move_client(self, client_info):
        """
        Determine if a client should be moved to the AFK channel based on the channel IDs and mode.
        """
        client_channel_id = int(client_info['cid'])
        client_idle_time = client_info['client_idle_time']

        # If the user is not AFK, don't move them.
        if not self.is_user_afk(client_idle_time):
            return False

        # Use should_process_channel to determine if the client should be moved
        return TeamSpeakAFKBot.should_process_channel(client_channel_id, self.afk_channel_id, self.mode, self.channel_ids)

    def run(self):
        """
        Main loop that checks clients and moves them to the AFK channel if necessary.
        """
        try:
            self.ts3_api.connect()
            self.ts3_api.use(self.server_id)
        except Exception as e:
            logging.error(f"An error occurred while connecting to the server: {e}")
            return

        while True:
            try:
                clients = self.ts3_api.get_clients()
                if not clients:
                    logging.info("No clients were retrieved from the server.")
                    continue

                for client in clients:
                    client_id = client.get('clid')
                    if not client_id:
                        logging.warning(f"Client data does not contain 'clid', skipping this client: {client}")
                        continue

                    try:
                        client_info = self.ts3_api.get_client_info(client_id)
                        if not client_info:
                            logging.warning(f"No info retrieved for client with ID {client_id}")
                            continue

                        if self.should_move_client(client_info):
                            self.move_client_to_afk(client_info)
                    except Exception as e:
                        logging.error(f"An error occurred while processing client with ID {client_id}: {e}")


            except Exception as e:
                logging.error(f"An error occurred during main loop: {e}")
                # Add a delay before retrying
                self.ts3_api.sleep(10)

            self.ts3_api.sleep(60)